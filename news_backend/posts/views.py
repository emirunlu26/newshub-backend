"""View module that contains all view functions to handle requests related to posts"""
from django.shortcuts import render

# Create your views here.

def add_post(request):
    """View function that handles the request for an user to create a post"""
    pass

def view_update_delete_post(request, post_id):
    """View function that handles the request for an user to view/update/delete a specific post"""
    pass

def add_update_view_delete_reaction_to_post(request, post_id):
    """View function that handles the request for an user to add/view/change/delete reaction to a post"""
    pass

def reference_post(request, post_id):
    """View function that handles the request for an user to reference a post"""
    pass

def view_post_form(request):
    """View function that returns a form to the requesting user to create a post"""
    pass
