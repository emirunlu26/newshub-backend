"""View module that contains all view functions to handle requests related to posts"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="users:login")
def add_post(request):
    """View function that handles the request for a user to create a post"""
    pass

def add_comment(request, post_id):
    """View function that handles the request for a user to create a comment"""
    pass

@login_required(login_url="users:login")
def view_update_delete_post(request, post_id):
    """View function that handles the request for a user to view/update/delete a specific post"""
    pass

@login_required(login_url="users:login")
def view_update_delete_comment(request, post_id):
    """View function that handles the request for a user to view/update/delete a specific comment"""
    pass

@login_required(login_url="users:login")
def view_add_update_delete_reaction_to_post(request, post_id):
    """View function that handles the request for a user to add/view/change/delete reaction to a post"""
    pass

@login_required(login_url="users:login")
def view_add_update_delete_reaction_to_comment(request, post_id):
    """View function that handles the request for a user to add/view/change/delete reaction to a comment"""
    pass

@login_required(login_url="users:login")
def reference_post(request, post_id):
    """View function that handles the request for a user to reference a post"""
    pass
