"""View file that contains all view functions to handle requests related to users"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from . import services
import json

# Create your views here.

def register_user(request):
    """View function that handles the request to register the requesting anonymous user"""
    if request.method == "POST":
        try:
            register_data = json.loads(request.body)
        except:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid JSON.",
                    "type": "error"
                }
            }, status=400)
        register_data["request"] = request
        response = services.register_user(register_data)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "POST request required.",
                "type": "error"
            }
        }, status=405)

def login_user(request):
    """View function that handles the request to login the requesting anonymous user"""
    if request.user.is_authenticated:
        return JsonResponse(data={
            "message": {
                "content": "You're already logged in.",
                "type": "info"
            },
            "redirect_url": ""
        }, status=400)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid JSON.",
                    "type": "error"
                }
            }, status=400)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request=request, username=username, password=password)
        credentials_valid = user is not None

        if credentials_valid:
            login(request=request, user=user)
            return JsonResponse(data={
                "message": {
                    "content": "Login successful ...",
                    "type": "success"
                },
                "redirect_url": "/homepage",
                "user": {
                    "id": user.id,
                    "username": user.username
                }
            }, status=200)
        else:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid credentials.",
                    "type": "error"
                }
            }, status=401)
    else:
        return JsonResponse(data={
            "message": {
                "content": "POST request required.",
                "type": "error"
            }
        }, status=405)



def logout_user(request):
    """View function that handles the request to logout the requesting user"""
    logout(request)
    return JsonResponse(data={
        "message": {
            "content": "Logout successful ...",
            "type": "success"
        },
        "redirect_url": "",
    }, status=200)

def get_profile(request, target_user_id):
    """View function that returns information about the profile of a specific user"""
    if request.method == "GET":
        requesting_user_id = request.user.id if request.user.is_authenticated else None
        response = services.get_profile(requesting_user_id, target_user_id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_profile_picture(request, user_id):
    """View function that returns the profile picture of a specific user"""
    if request.method == "GET":
        response = services.get_profile_picture(user_id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_following_list(request, user_id):
    """View function that returns the list of users which is followed by a specific user"""
    if request.method == "GET":
        response = services.get_following_list(requesting_user_id=request.user.id, target_user_id=user_id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_follower_list(request, user_id):
    """View function that returns the list of users following a specific user"""
    if request.method == "GET":
        response = services.get_following_list(requesting_user_id=request.user.id, target_user_id=user_id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_followed_tags(request):
    """View function that returns the list of tags which is followed by the requesting user"""
    if request.method == "GET":
        response = services.get_followed_tags(requesting_user_id=request.user.id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_followed_categories(request):
    """View function that returns the list of categories which is followed by the requesting user"""
    if request.method == "GET":
        response = services.get_followed_categories(requesting_user_id=request.user.id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_bookmarked_articles(request):
    """View function that returns the list of articles which is bookmarked by the requesting user"""
    if request.method == "GET":
        response = services.get_bookmarked_articles(requesting_user_id=request.user.id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_update_profile_settings(request):
    """View function that either returns or updates the profile settings of the requesting user"""
    if request.method == "GET":
        response = services.get_profile_settings(request.user.id)
        return JsonResponse(data=response, status=response["message"]["status"])
    elif request.method == "PUT":
        try:
            update_data = json.loads(request.body)
        except:
            return JsonResponse(data=
            {
                "message": {
                    "content": "Invalid JSON.",
                    "type": "error"
                }
            }, status=400)
        response = services.update_profile_settings(request.user.id, update_data)
        FIRST_MESSAGE_INDEX = 0
        return JsonResponse(data=response, status=response["messages"][FIRST_MESSAGE_INDEX]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET or PUT request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_update_ui_customization_settings(request):
    """View function that either returns or updates the user interface customization settings of the requesting user"""
    if request.method == "GET":
        response = services.get_ui_customization_settings(request.user.id)
        return JsonResponse(data=response, status=response["message"]["status"])
    elif request.method == "PUT":
        try:
            update_data = json.loads(request.body)
        except:
            return JsonResponse(data=
            {
                "message": {
                    "content": "Invalid JSON.",
                    "type": "error"
                }
            }, status=400)
        response = services.update_ui_customization_settings(request.user.id, update_data)
        FIRST_MESSAGE_INDEX = 0
        return JsonResponse(data=response, status=response["messages"][FIRST_MESSAGE_INDEX]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET or PUT request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def subscribe_or_unsubscribe(request):
    """View function that handles the request about subscription/unsubscription of the requesting user"""
    if request.method == "POST":
        response = services.subscribe_user(request.user.id)
    elif request.method == "DELETE":
        response = services.unsubscribe_user(request.user.id)
    else:
        return JsonResponse(data={
            "message": {
                "content": "POST or DELETE request required.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=response["message"]["status"])


@login_required(login_url="users:login")
def follow_or_unfollow(request, target_user_id):
    """View the function that handles the request about requesting user following/unfollowing a specific user"""
    if request.method == "POST":
        response = services.follow_user(request.user.id, target_user_id)
    elif request.method == "DELETE":
        response = services.unfollow_user(request.user.id, target_user_id)
    else:
        return JsonResponse(data={
            "message": {
                "content": "POST or DELETE request required.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=response["message"]["status"])

