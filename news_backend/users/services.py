"""Service file representing the service layer of the project.
It contains all service functions to handle requests related to users
Service functions implement the business logic.
"""
from django.contrib.auth import login
from .models import User, UserProfile
import users.serializers as user_serializers
from articles import serializers as article_serializers

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
    birth_date = register_data.get("birth_date")

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
    if birth_date is None:
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

    # Create the user and set the required & optional fields
    new_user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    country=country,
                                    birth_date=birth_date,
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
    requesting_user = User.objects.filter(id=requesting_user_id).first()
    if requesting_user is None:
        return {
            "message": {
                "content": "Requesting user with the given id is not found.",
                "type": "error"
            }
        }, 404

    target_user = User.objects.filter(id=target_user_id).first()
    if target_user is None:
        return {
            "message": {
                "content": "Target user with the given id is not found.",
                "type": "error"
            }
        }, 404

    following_list = target_user.following_list.all()
    sorted_following_list = User.get_sorted_following_or_follower_list(requesting_user=requesting_user
                                                                       , following_or_follower_list=following_list)
    sorted_following_list = [user_serializers.serialize_user(user) for user in sorted_following_list]
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
    requesting_user = User.objects.filter(id=requesting_user_id).first()
    if requesting_user is None:
        return {
            "message": {
                "content": "Requesting user with the given id is not found.",
                "type": "error"
            }
        }, 404

    target_user = User.objects.filter(id=target_user_id).first()
    if target_user is None:
        return {
            "message": {
                "content": "Target user with the given id is not found.",
                "type": "error"
            }
        }, 404

    followers = target_user.followers.all()
    sorted_followers = User.get_sorted_following_or_follower_list(requesting_user=requesting_user
                                                                       , following_or_follower_list=followers)
    sorted_followers = [user_serializers.serialize_user(user) for user in sorted_followers]
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
    requesting_user = User.objects.filter(id=requesting_user_id).first()
    if requesting_user is None:
        return {
            "message": {
                "content": "Requesting user with the given id is not found.",
                "type": "error"
            }
        }, 404

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
    requesting_user = User.objects.filter(id=requesting_user_id).first()
    if requesting_user is None:
        return {
            "message": {
                "content": "Requesting user with the given id is not found.",
                "type": "error"
            }
        }, 404

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
    requesting_user = User.objects.filter(id=requesting_user_id).first()
    if requesting_user is None:
        return {
            "message": {
                "content": "Requesting user with the given id is not found.",
                "type": "error"
            }
        }, 404

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



