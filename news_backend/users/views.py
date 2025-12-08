"""View module that contains all view functions to handle requests related to users"""
from django.shortcuts import render

# Create your views here.

def view_profile(request, user_id):
    """View function that returns information about the profile of a specific user"""
    pass

def view_profile_picture(request, user_id):
    """View function that returns the profile picture of a specific user"""
    pass

def view_following_list(request, user_id):
    """View function that returns the list of users which is followed by a specific user"""
    pass

def view_follower_list(request, user_id):
    """View function that returns the list of users following a specific user"""
    pass

def view_followed_tags(request):
    """View function that returns the list of tags which is followed by the requesting user"""
    pass

def view_followed_categories(request):
    """View function that returns the list of categories which is followed by the requesting user"""
    pass

def view_bookmarked_articles(request):
    """View function that returns the list of articles which is bookmarked by the requesting user"""
    pass

def view_profile_settings(request):
    """View function that returns the information about profile settings of the requesting user"""
    pass

def view_ui_customization_settings(request):
    """View function that returns the information about user interface customization settings of the requesting user"""
    pass

def subscribe_or_unsubscribe(request):
    """View function that handles the request about subscription/unsubscription of the requesting user"""
    pass

def follow_or_unfollow(request, user_id):
    """View the function that handles the request about requesting user following/unfollowing a specific user"""
    pass

