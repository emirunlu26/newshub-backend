"""Service file representing the service layer of the project.
It contains all service functions to handle requests related to users
Service functions implement the business logic.
"""
from django.contrib.auth import login
from .models import User, UserProfile
from django.contrib.auth.models import Group
import users.serializers as user_serializers
from articles import serializers as article_serializers
from news_backend import settings
from datetime import datetime

def get_user_by_id(id, user_type="Requesting"):
    user = User.objects.filter(id=id).first()
    if user:
        return {
            "message": {
                "content": user_type + " " + "user is retrieved successfully.",
                "type": "success"
            },
            "user": user
        }, 200
    else:
        return user, {
            "message": {
                "content": "User with the given id is not found.",
                "type": "error"
            },
            "user": None
        }, 404


def register_user(register_data):
    """Service function that registers an user"""
    # Get request:
    request = register_data.get["request"]

    # Get required fields
    username = register_data.get("username")
    password = register_data.get("password")
    password_repeat = register_data.get("password_repeat")
    first_name = register_data.get("first_name")
    last_name = register_data.get("last_name")
    email = register_data.get("email")
    country = register_data.get("country")
    birth_date_str = register_data.get("birth_date")

    # Get optional fields
    gender = register_data.get("gender")

    # Check if the required fields are not empty
    if username is None:
        return {"message": {"content": "User Name field can not be empty.", "type": "error"}}, 400
    if password is None:
        return {"message": {"content": "Password field can not be empty.", "type": "error"}}, 400
    if password_repeat is None:
        return {"message": {"content": "Password must be repeated for validaton.", "type": "error"}}, 400
    if first_name is None:
        return {"message": {"content": "First Name field can not be empty.", "type": "error"}}, 400
    if last_name is None:
        return {"message": {"content": "Last Name field can not be empty.", "type": "error"}}, 400
    if email is None:
        return {"message": {"content": "Email field can not be empty.", "type": "error"}}, 400
    if country is None:
        return {"message": {"content": "Location field can not be empty.", "type": "error"}}, 400
    if birth_date_str is None:
        return {"message": {"content": "Birth date field can not be empty.", "type": "error"}}, 400

    # Check if username and email are unique:
    if User.objects.filter(username=username).exists():
        return {"message": {"content": "This user name is already used by an existing account.", "type": "error"}}, 400
    if User.objects.filter(email=email).exists():
        return {"message": {"content": "This email is already used by an existing account.", "type": "error"}}, 400

    # Check if username and password are valid
    if not User.is_username_valid(username):
        return {"message": {"content": "Invalid user name.", "type": "error"}}, 400
    if not User.is_password_valid(password):
        return {"message": {"content": "Invalid password.", "type": "error"}}, 400

    # Check if the repeated password matches with first password
    if password != password_repeat:
        return {"message": {"content": "Repeated password is different.", "type": "error"}}, 400

    if not User.is_birth_date_valid(birth_date_str):
        return {"message":
                    {"content": f"Invalid birth date. Accepted format is: {settings.DATE_INPUT_FORMATS[0]}",
                     "type": "error"
                     }
                }, 400

    # Create the user and set the required & optional fields
    new_user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    country=country,
                                    birth_date=datetime.strptime(birth_date_str, settings.DATE_INPUT_FORMATS[0]).date(),
                                    gender=gender)
    new_user.save()
    create_profile_for_new_user(new_user)
    login(request=request, user=new_user)
    return {
        "message": {
            "content": "User created successfully",
            "type": "success"},
        "user_id": new_user.id,
        "redirect_url": ""
    }, 201

def create_profile_for_new_user(user):
    user_profile = UserProfile.objects.create(user=user)
    user_profile.save()

def view_following_list(requesting_user_id, target_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]

    response, status = get_user_by_id(target_user_id, user_type="Target")
    if not response["user"]:
        return response, status

    target_user = response["user"]
    following_list = target_user.following_list.all()
    sorted_following_list = User.get_sorted_following_or_follower_list(requesting_user=requesting_user
                                                                       , following_or_follower_list=following_list)
    sorted_following_list = [user_serializers.serialize_user_teaser(user) for user in sorted_following_list]
    following_count = len(sorted_following_list)

    return {
        "message": {
            "content": "The list of followed users is retrieved successfully.",
            "type": "success"
        },
        "following_count": following_count,
        "following_list": sorted_following_list
    }, 200

def view_follower_list(requesting_user_id, target_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]

    response, status = get_user_by_id(target_user_id, user_type="Target")
    if not response["user"]:
        return response, status

    target_user = response["user"]
    followers = target_user.followers.all()
    sorted_followers = User.get_sorted_following_or_follower_list(requesting_user=requesting_user
                                                                       , following_or_follower_list=followers)
    sorted_followers = [user_serializers.serialize_user_teaser(user) for user in sorted_followers]
    follower_count = len(sorted_followers)

    return {
        "message": {
            "content": "The list of followers is retrieved successfully.",
            "type": "success"
        },
        "follower_count": follower_count,
        "followers": sorted_followers
    }, 200

def view_followed_tags(requesting_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]
    sorted_followed_tags = requesting_user.get_sorted_followed_tags()
    sorted_followed_tags = [article_serializers.serialize_tag(tag) for tag in sorted_followed_tags]

    return {
        "message": {
            "content": "The list of followed tags is retrieved successfully.",
            "type": "success"
        },
        "followed_tags": sorted_followed_tags
    }, 200

def view_followed_categories(requesting_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]
    sorted_followed_categories = requesting_user.get_sorted_followed_categories()
    sorted_followed_categories = [article_serializers.serialize_category(category)
                                  for category in sorted_followed_categories]

    return {
        "message": {
            "content": "The list of followed categories is retrieved successfully.",
            "type": "success"
        },
        "followed_categories": sorted_followed_categories
    }, 200

def view_bookmarked_articles(requesting_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]
    sorted_bookmarked_articles = requesting_user.get_sorted_bookmarked_articles()
    sorted_bookmarked_articles = [article_serializers.serialize_article_teaser(article)
                                  for article in sorted_bookmarked_articles]

    return {
        "message": {
            "content": "The list of bookmarked articles is retrieved successfully.",
            "type": "success"
        },
        "bookmarked_articles": sorted_bookmarked_articles
    }, 200

def subscribe_user(requesting_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]
    if requesting_user.profile.is_premium():
        return {
            "message": {
                "content": "Your account has already been premium.",
                "type": "warning"
            }
        }, 200

    premium_group = Group.objects.get_or_create(name="premium")
    requesting_user.groups.add(premium_group)
    return {
        "message": {
            "content": "Your account is upgraded to premium successfully.",
            "type": "success"
        },
        "redirect_url": ""
    }, 200


def unsubscribe_user(requesting_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]
    if not requesting_user.profile.is_premium():
        return {
            "message": {
                "content": "Your account has already been not premium.",
                "type": "warning"
            }
        }, 200

    premium_group = Group.objects.get_or_create(name="premium")
    requesting_user.groups.remove(premium_group)
    return {
        "message": {
            "content": "Your subscription has been terminated successfully.",
            "type": "success"
        },
        "redirect_url": ""
    }, 200

def follow_user(requesting_user_id, target_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]

    response, status = get_user_by_id(target_user_id, user_type="Target")
    if not response["user"]:
        return response, status

    target_user = response["user"]
    if requesting_user.follows_user(target_user):
        return {
            "message": {
                "content": "You're already following this user.",
                "type": "warning"
            }
        }, 200
    else:
        requesting_user.followers.add(target_user)
        return {
            "message": {
                "content": "User is followed successfully.",
                "type": "success"
            }
        }, 200


def unfollow_user(requesting_user_id, target_user_id):
    response, status = get_user_by_id(requesting_user_id)
    if not response["user"]:
        return response, status

    requesting_user = response["user"]

    response, status = get_user_by_id(target_user_id, "Target")
    if not response["user"]:
        return response, status

    target_user = response["user"]
    if requesting_user.follows_user(target_user):
        requesting_user.followers.remove(target_user)
        return {
            "message": {
                "content": "User is unfollowed successfully.",
                "type": "warning"
            }
        }, 200
    else:
        requesting_user.followers.add(target_user)
        return {
            "message": {
                "content": "You're not following this user already.",
                "type": "success"
            }
        }, 200

def view_profile_picture(target_user_id):
    response, status = get_user_by_id(target_user_id, user_type="Target")
    if not response["user"]:
        return response, status

    target_user = response["user"]
    avatar = target_user.profile.avatar
    return {
        "message": {
            "content": "Profile picture is retrieved successfully.",
            "type": "success"
        },
        "profile_picture_url": avatar.url if avatar else None
    }, 200

def view_profile_settings(user_id):
    response, status = get_user_by_id(user_id)
    if not response["user"]:
        return response, status

    user = response["user"]
    profile = user.profile
    return {
        "message": "Profile settings are retrieved successfully.",
        "type": "success",
        "profile_settings": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date.strftime(settings.DATE_INPUT_FORMATS[0]),
            "gender": user.gender,
            "profile_bio": profile.bio,
            "avatar": profile.avatar.url if profile.avatar else None
        }
    }, 200

def update_profile_settings(user_id, update_data):
    response, status = get_user_by_id(user_id)
    if not response["user"]:
        return response, status

    user = response["user"]
    profile = user.profile

    username = update_data.get("username")
    first_name = update_data.get("first_name")
    last_name = update_data.get("last_name")
    birth_date_str = update_data.get("birth_date")
    gender = update_data.get("gender")
    profile_bio = update_data.get("profile_bio")

    if username and user.username != username:
        if User.objects.filter(username=username).exists():
            return {
                "message": {
                    "content": "This user name is already used by another account.",
                    "type": "error"
                }
            }, 400
        elif not User.is_username_valid(username):
            return {
                "message": {
                    "content": "Invalid username.",
                    "type": "error"
                }
            }, 400
        else:
            user.username = username
            user.save()

    if first_name and first_name != user.first_name:
        user.first_name = first_name
        user.save()
    if last_name and last_name != user.last_name:
        user.last_name = last_name
        user.save()
    if birth_date_str:
        if User.is_birth_date_valid(birth_date_str):
            birth_date = datetime.strptime(birth_date_str, settings.DATE_INPUT_FORMATS[0]).date()
            user.birth_date = birth_date
            user.save()
        else:
            return {
                "message": {
                    "content": f"Invalid birth date. Accepted format is: {settings.DATE_INPUT_FORMATS[0]}",
                    "type": "error"
                }
            }, 400

    if gender and gender != user.gender:
        if User.is_gender_valid(gender):
            user.gender = gender
            user.save()
        else:
            return {
                "message": {
                    "content": "Invalid gender.",
                    "type": "error"
                }
            }, 400

    if profile_bio and profile_bio != profile_bio:
        profile.bio = profile_bio
        profile.save()

    return {
        "message": {
            "content": "Profile settings are updated successfully.",
            "type": "error"
        },
        "profile_settings": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date.strftime(settings.DATE_INPUT_FORMATS[0]),
            "gender": user.gender,
            "profile_bio": profile.bio,
            "avatar": profile.avatar.url if profile.avatar else None
        }
    }, 200
