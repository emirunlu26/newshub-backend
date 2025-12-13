"""View module that contains all view functions to handle requests related to posts"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import services as post_services
import json

# Create your views here.

@login_required(login_url="users:login")
def create_post(request):
    """View function that handles the request for a user to create a post"""
    pass

@login_required(login_url="users:login")
def create_comment(request, post_id):
    """View function that handles the request for a user to create a comment"""
    if request.method == "POST":
        try:
            create_data = json.loads(request.body)
        except:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid JSON",
                    "type": "error"
                },
            }, status=400)
        response, status = post_services.create_comment(request.user.id, post_id, create_data)
        return JsonResponse(data=response, status=status)
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def view_update_delete_post(request, post_id):
    """View function that handles the request for a user to view/update/delete a specific post"""
    if request.method == "GET":
        response, status =  post_services.get_post_by_id(post_id)
    elif request.method == "PUT":
        try:
            update_data = json.loads(request.body)
        except:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid JSON",
                    "type": "error"
                },
            }, status=400)
        response, status = post_services.update_post_by_id(request.user.id, post_id, update_data)
    elif request.method == "DELETE":
        response, status = post_services.delete_post_by_id(request.user.id, post_id)
    else:
        return JsonResponse(data={
            "message": {
                "content": "Only GET, PUT and DELETE request required.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=status)

@login_required(login_url="users:login")
def view_update_delete_comment(request, post_id):
    """View function that handles the request for a user to view/update/delete a specific comment"""
    if request.method == "GET":
        response, status = post_services.get_comment_by_id(post_id)
    elif request.method == "PUT":
        try:
            update_data = json.loads(request.body)
        except:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid JSON",
                    "type": "error"
                },
            }, status=400)
        response, status = post_services.update_comment_by_id(request.user.id, post_id, update_data)
    elif request.method == "DELETE":
        response, status = post_services.delete_comment_by_id(request.user.id, post_id)
    else:
        return JsonResponse(data={
            "message": {
                "content": "Only GET, PUT and DELETE request required.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=status)

@login_required(login_url="users:login")
def create_view_update_delete_reaction_to_post(request, post_id):
    """View function that handles the request for a user to add/view/change/delete reaction to a post"""
    pass

@login_required(login_url="users:login")
def create_view_update_delete_reaction_to_comment(request, post_id):
    """View function that handles the request for a user to add/view/change/delete reaction to a comment"""
    pass

@login_required(login_url="users:login")
def reference_post(request, post_id):
    """View function that handles the request for a user to reference a post"""
    pass
