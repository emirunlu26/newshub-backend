"""Service file representing the service layer of the project.
It contains all service functions to handle requests related to users
Service functions implement the business logic.
"""
from django.contrib.auth import login
from .models import User, UserProfile, UserCustomization
from django.contrib.auth.models import Group
import users.serializers as user_serializers
from articles import serializers as article_serializers
from news_backend import settings
from datetime import datetime

def get_user_by_id_helper(id, user_type="Requesting"):
    user = User.objects.filter(id=id).first()
    if user:
        return {
            "message": {
                "content": user_type + " " + "user with the given id retrieved successfully",
                "type": "success",
                "status": 200
            },
            "user": user
        }
    else:
        return {
            "message": {
                "content": "User with the given id is not found.",
                "type": "error",
                "status": 404
            },
            "user": None
        }


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
        return {"message": {"content": "User Name field can not be empty.", "type": "error", "status": 400}}
    if password is None:
        return {"message": {"content": "Password field can not be empty.", "type": "error", "status": 400}}
    if password_repeat is None:
        return {"message": {"content": "Password must be repeated for validaton.", "type": "error", "status": 400}}
    if first_name is None:
        return {"message": {"content": "First Name field can not be empty.", "type": "error", "status": 400}}
    if last_name is None:
        return {"message": {"content": "Last Name field can not be empty.", "type": "error", "status": 400}}
    if email is None:
        return {"message": {"content": "Email field can not be empty.", "type": "error", "status": 400}}
    if country is None:
        return {"message": {"content": "Location field can not be empty.", "type": "error", "status": 400}}
    if birth_date_str is None:
        return {"message": {"content": "Birth date field can not be empty.", "type": "error", "status": 400}}

    # Check if username and email are unique:
    if User.objects.filter(username=username).exists():
        return {"message": {
            "content": "This user name is already used by an existing account.", "type": "error", "status": 400
        }}
    if User.objects.filter(email=email).exists():
        return {"message": {
            "content": "This email is already used by an existing account.", "type": "error", "status": 400
        }}

    # Check if username and password are valid
    if not User.is_username_valid(username):
        return {"message": {"content": "Invalid user name.", "type": "error", "status": 400}}
    if not User.is_password_valid(password):
        return {"message": {"content": "Invalid password.", "type": "error", "status": 400}}

    # Check if the repeated password matches with first password
    if password != password_repeat:
        return {"message": {"content": "Repeated password is different.", "type": "error", "status": 400}}

    if not User.is_birth_date_valid(birth_date_str):
        return {"message":
                    {
                        "content": f"Invalid birth date. Accepted format is: {settings.DATE_INPUT_FORMATS[0]}",
                        "type": "error",
                        "status": 400
                    }
                }

    # Create the user and set the required & optional fields
    new_user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    country=country,
                                    birth_date=datetime.strptime(birth_date_str, settings.DATE_INPUT_FORMATS[0]).date(),
                                    gender=gender)
    create_profile_for_new_user_helper(new_user)
    login(request=request, user=new_user)
    return {
        "message": {
            "content": "User created successfully",
            "type": "success",
            "status": 201
        },
        "user_id": new_user.id,
        "redirect_url": ""
    }

def create_profile_for_new_user_helper(user):
    user_profile = UserProfile.objects.create(user=user)

def view_following_list(requesting_user_id, target_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_user_by_id_helper(target_user_id, user_type="Target")
    if not response["user"]:
        return response

    target_user = response["user"]
    following_list = target_user.following_list.all()
    sorted_following_list = User.get_sorted_following_or_follower_list(requesting_user=requesting_user
                                                                       , following_or_follower_list=following_list)
    sorted_following_list = [user_serializers.serialize_user_teaser(user) for user in sorted_following_list]
    following_count = len(sorted_following_list)

    return {
        "message": {
            "content": "The list of followed users is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "following_count": following_count,
        "following_list": sorted_following_list
    }

def view_follower_list(requesting_user_id, target_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_user_by_id_helper(target_user_id, user_type="Target")
    if not response["user"]:
        return response

    target_user = response["user"]
    followers = target_user.followers.all()
    sorted_followers = User.get_sorted_following_or_follower_list(requesting_user=requesting_user
                                                                       , following_or_follower_list=followers)
    sorted_followers = [user_serializers.serialize_user_teaser(user) for user in sorted_followers]
    follower_count = len(sorted_followers)

    return {
        "message": {
            "content": "The list of followers is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "follower_count": follower_count,
        "followers": sorted_followers
    }

def view_followed_tags(requesting_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]
    sorted_followed_tags = requesting_user.get_sorted_followed_tags()
    sorted_followed_tags = [article_serializers.serialize_tag(tag) for tag in sorted_followed_tags]

    return {
        "message": {
            "content": "The list of followed tags is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "followed_tags": sorted_followed_tags
    }

def view_followed_categories(requesting_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]
    sorted_followed_categories = requesting_user.get_sorted_followed_categories()
    sorted_followed_categories = [article_serializers.serialize_category(category)
                                  for category in sorted_followed_categories]

    return {
        "message": {
            "content": "The list of followed categories is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "followed_categories": sorted_followed_categories
    }

def view_bookmarked_articles(requesting_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]
    sorted_bookmarked_articles = requesting_user.get_sorted_bookmarked_articles()
    sorted_bookmarked_articles = [article_serializers.serialize_article_teaser(article)
                                  for article in sorted_bookmarked_articles]

    return {
        "message": {
            "content": "The list of bookmarked articles is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "bookmarked_articles": sorted_bookmarked_articles
    }

def subscribe_user(requesting_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]
    if requesting_user.profile.is_premium():
        return {
            "message": {
                "content": "Your account has already been premium.",
                "type": "warning",
                "status": 200
            }
        }

    premium_group = Group.objects.get_or_create(name="premium")
    requesting_user.groups.add(premium_group)
    return {
        "message": {
            "content": "Your account is upgraded to premium successfully.",
            "type": "success",
            "status": 200
        },
        "redirect_url": ""
    }


def unsubscribe_user(requesting_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]
    if not requesting_user.profile.is_premium():
        return {
            "message": {
                "content": "Your account has already been not premium.",
                "type": "warning",
                "status": 200
            }
        }

    premium_group = Group.objects.get_or_create(name="premium")
    requesting_user.groups.remove(premium_group)
    return {
        "message": {
            "content": "Your subscription has been terminated successfully.",
            "type": "success",
            "status": 200
        },
        "redirect_url": ""
    }

def follow_user(requesting_user_id, target_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_user_by_id_helper(target_user_id, user_type="Target")
    if not response["user"]:
        return response

    target_user = response["user"]
    if requesting_user.follows_user(target_user):
        return {
            "message": {
                "content": "You're already following this user.",
                "type": "warning",
                "status": 200
            }
        }
    else:
        requesting_user.followers.add(target_user)
        return {
            "message": {
                "content": "User is followed successfully.",
                "type": "success",
                "status": 200
            }
        }


def unfollow_user(requesting_user_id, target_user_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_user_by_id_helper(target_user_id, "Target")
    if not response["user"]:
        return response

    target_user = response["user"]
    if requesting_user.follows_user(target_user):
        requesting_user.following_list.remove(target_user)
        return {
            "message": {
                "content": "User is unfollowed successfully.",
                "type": "success",
                "status": 200
            }
        }
    else:
        return {
            "message": {
                "content": "You're not following this user already.",
                "type": "warning",
                "status": 200
            }
        }

def view_profile_picture(target_user_id):
    response = get_user_by_id_helper(target_user_id, user_type="Target")
    if not response["user"]:
        return response

    target_user = response["user"]
    avatar = target_user.profile.avatar
    return {
        "message": {
            "content": "Profile picture is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "profile_picture_url": avatar.url if avatar else None
    }

def view_profile_settings(user_id):
    response = get_user_by_id_helper(user_id)
    if not response["user"]:
        return response

    user = response["user"]
    profile = user.profile
    return {
        "message": {
            "content": "Profile settings are retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "profile_settings": user_serializers.serialize_user_profile(profile)
    }

def update_profile_settings(user_id, update_data):
    response = get_user_by_id_helper(user_id)
    if not response["user"]:
        return response

    user = response["user"]
    profile = user.profile

    username = update_data.get("username")
    first_name = update_data.get("first_name")
    last_name = update_data.get("last_name")
    birth_date_str = update_data.get("birth_date")
    gender = update_data.get("gender")
    profile_bio = update_data.get("profile_bio")

    check_dict = {
        "error_messages": [],
        "valid_update_data": {}
    }

    if username and user.username != username:
        if User.objects.filter(username=username).exists():
            check_dict["error_messages"].append(
                {
                    "content": "This user name is already used by another account.",
                    "type": "error",
                    "status": 400
                }
            )
        elif not User.is_username_valid(username):
            check_dict["error_messages"].append(
                {
                    "content": "Invalid username.",
                    "type": "error",
                    "status": 400
                }
            )
        else:
            check_dict["valid_update_data"]["username"] = username

    if first_name and first_name != user.first_name:
        check_dict["valid_update_data"]["first_name"] = first_name
    if last_name and last_name != user.last_name:
        check_dict["valid_update_data"]["last_name"] = last_name
    if birth_date_str:
        if User.is_birth_date_valid(birth_date_str):
            birth_date = datetime.strptime(birth_date_str, settings.DATE_INPUT_FORMATS[0]).date()
            check_dict["valid_update_data"]["birth_date"] = birth_date
        else:
            check_dict["error_messages"].append(
                {
                    "content": f"Invalid birth date. Accepted format is: {settings.DATE_INPUT_FORMATS[0]}",
                    "type": "error",
                    "status": 400
                }
            )

    if gender and gender != user.gender:
        if User.is_gender_valid(gender):
            check_dict["valid_update_data"]["gender"] = gender
        else:
            check_dict["error_messages"].append(
                {
                    "content": "Invalid gender.",
                    "type": "error",
                    "status": 400
                }
            )

    if profile_bio and profile_bio != profile_bio:
        check_dict["valid_update_data"]["profile_bio"] = profile_bio

    # If there is any error, return all error messages. Otherwise, update data with the validated data.
    if check_dict["error_messages"]:
        return {
            "messages": check_dict["error_messages"]
        }
    else:
        if "username" in check_dict["valid_update_data"]:
            user.username = check_dict["valid_update_data"]["username"]

        if "first_name" in check_dict["valid_update_data"]:
            user.first_name = check_dict["valid_update_data"]["first_name"]

        if "last_name" in check_dict["valid_update_data"]:
            user.last_name = check_dict["valid_update_data"]["last_name"]

        if "birth_date" in check_dict["valid_update_data"]:
            user.birth_date = check_dict["valid_update_data"]["birth_date"]

        if "gender" in check_dict["valid_update_data"]:
            user.gender = check_dict["valid_update_data"]["gender"]

        if "profile_bio" in check_dict["valid_update_data"]:
            profile.bio = check_dict["valid_update_data"]["profile_bio"]

        # Save updates
        user.save()
        profile.save()

        return {
            "message": {
                "content": "Profile settings are updated successfully.",
                "type": "success",
                "status": 200
            },
            "profile_settings": user_serializers.serialize_user_profile(profile)
        }

def view_ui_customization_settings(user_id):
    response = get_user_by_id_helper(user_id)
    if not response["user"]:
        return response

    user = response["user"]
    ui_customization_json = user_serializers.serialize_ui_customization(user.customization)
    return {
        "message": {
            "content": "UI customization setting is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "customization": ui_customization_json
    }

def update_ui_customization_settings(user_id, update_data):
    response = get_user_by_id_helper(user_id)
    if not response["user"]:
        return response

    user = response["user"]
    customization = user.customization

    theme = update_data.get("theme")
    font_type = update_data.get("font_type")
    font_size_str = update_data.get("font_size")
    font_colour = update_data.get("font_colour")

    check_dict = {
        "error_messages": [],
        "valid_update_data": {}
    }

    if theme and theme != customization.theme:
        if UserCustomization.is_theme_valid(theme):
            check_dict["valid_update_data"]["theme"] = theme
        else:
            check_dict["error_messages"].append(
                {
                    "content": "Invalid theme.",
                    "type": "error",
                    "status": 400
                }
            )
    if font_type:
        if UserCustomization.is_font_type_valid(font_type):
            check_dict["valid_update_data"]["font_type"] = font_type
        else:
            check_dict["error_messages"].append(
                {
                    "content": "Invalid font type.",
                    "type": "error",
                    "status": 400
                }
            )

    if font_size_str:
        if UserCustomization.is_font_size_valid(font_size_str):
            check_dict["valid_update_data"]["font_size"] = int(font_size_str)
        else:
            check_dict["error_messages"].append(
                {
                    "content": "Invalid font size.",
                    "type": "error",
                    "status": 400
                }
            )
    if font_colour:
        if UserCustomization.is_font_colour_valid(font_colour):
            check_dict["valid_update_data"]["font_colour"] = font_colour
        else:
            check_dict["error_messages"].append(
                {
                    "content": "Invalid font colour.",
                    "type": "error",
                    "status": 400
                }
            )

    # If there is any error, return all error messages. Otherwise, update data with the validated data.
    if check_dict["error_messages"]:
        return {
            "messages": check_dict["error_messages"]
        }
    else:
        if "theme" in check_dict["valid_update_data"]:
            customization.theme = check_dict["valid_update_data"]["theme"]

        if "font_type" in check_dict["valid_update_data"]:
            customization.font_type = check_dict["valid_update_data"]["font_type"]

        if "font_size" in check_dict["valid_update_data"]:
            customization.font_size = check_dict["valid_update_data"]["font_size"]

        if "font_colour" in check_dict["valid_update_data"]:
            customization.font_colour = check_dict["valid_update_data"]["font_colour"]

        # Save update
        customization.save()

        return {
            "message": {
                "content": "UI customization settings are updated successfully.",
                "type": "success",
                "status": 200
            },
            "ui_customization": user_serializers.serialize_ui_customization(customization)
        }

def view_profile(requesting_user_id, target_user_id):
    requesting_user = None
    if requesting_user_id:
        response = get_user_by_id_helper(target_user_id)
        if response["user"]:
            requesting_user = response["user"]
        else:
            return response

    response = get_user_by_id_helper(target_user_id, user_type="Target")
    if not response["user"]:
        return response

    target_user = response["user"]
    target_profile = target_user.profile

    return {
        "message": {
            "content": "User profile is retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "profile": user_serializers.serialize_user_profile(target_profile),
        "target_user_followed": requesting_user.follows_user(target_user) if requesting_user else False
    }
