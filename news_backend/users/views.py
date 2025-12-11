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
        response, status = services.register_user(register_data)
        return JsonResponse(data=response, status=status)
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
        })
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
            })
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
    })

def view_profile(request, user_id):
    """View function that returns information about the profile of a specific user"""
    pass

def view_profile_picture(request, user_id):
    """View function that returns the profile picture of a specific user"""
    pass

@login_required(login_url="users:login")
def view_following_list(request, user_id):
    """View function that returns the list of users which is followed by a specific user"""
    if request.method == "GET":
        response, status = services.view_following_list(requesting_user_id=request.user.id, target_user_id=user_id)
        return JsonResponse(data=response, status=status)
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def view_follower_list(request, user_id):
    """View function that returns the list of users following a specific user"""
    if request.method == "GET":
        response, status = services.view_following_list(requesting_user_id=request.user.id, target_user_id=user_id)
        return JsonResponse(data=response, status=status)
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def view_followed_tags(request):
    """View function that returns the list of tags which is followed by the requesting user"""
    pass

@login_required(login_url="users:login")
def view_followed_categories(request):
    """View function that returns the list of categories which is followed by the requesting user"""
    pass

@login_required(login_url="users:login")
def view_bookmarked_articles(request):
    """View function that returns the list of articles which is bookmarked by the requesting user"""
    pass

@login_required(login_url="users:login")
def view_profile_settings(request):
    """View function that returns the information about profile settings of the requesting user"""
    pass

@login_required(login_url="users:login")
def view_ui_customization_settings(request):
    """View function that returns the information about user interface customization settings of the requesting user"""
    pass

@login_required(login_url="users:login")
def subscribe_or_unsubscribe(request):
    """View function that handles the request about subscription/unsubscription of the requesting user"""
    pass

@login_required(login_url="users:login")
def follow_or_unfollow(request, user_id):
    """View the function that handles the request about requesting user following/unfollowing a specific user"""
    pass

