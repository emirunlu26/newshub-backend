"""View module that contains all view functions to handle requests related to posts"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import services as post_services
import json

# Create your views here.

@login_required(login_url="users:login")
def create_post(request):
    """View function that handles the request for a user to create a post"""
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
        create_data["images"] = request.FILES.getList("images")
        response, status = post_services.create_post(request.user.id, create_data)
        return JsonResponse(data=response, status=status)
    else:
        return JsonResponse(data={
            "message": {
                "content": "POST request required.",
                "type": "error"
            }
        }, status=405)

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
                "content": "POST request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_update_delete_post(request, post_id):
    """View function that handles the request for a user to view/update/delete a specific post"""
    if request.method == "GET":
        response, status = post_services.get_post_by_id(post_id)
        return JsonResponse(data=response, status=status)
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
def get_delete_comment(request, post_id):
    """View function that handles the request for a user to view/delete a specific comment"""
    if request.method == "GET":
        response, status = post_services.get_comment_by_id(request.user.id, post_id)
    elif request.method == "DELETE":
        response, status = post_services.delete_comment_by_id(request.user.id, post_id)
    else:
        return JsonResponse(data={
            "message": {
                "content": "Only GET and DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=status)

@login_required(login_url="users:login")
def create_get_delete_reaction_to_post(request, post_id):
    """View function that handles the request for a user to add/view/change/delete reaction to a post"""
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
        response, status = post_services.create_reaction_to_post(request.user.id, post_id, create_data)

    elif request.method == "GET":
        response, status= post_services.get_reactions_to_post(request.user.id, post_id)

    elif request.method == "DELETE":
        response, status = post_services.delete_reaction_to_post(request.user.id, post_id)

    else:
        return JsonResponse(data={
            "message": {
                "content": "Only POST/GET//DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)

    return JsonResponse(data=response, status=status)

@login_required(login_url="users:login")
def create_get_delete_reaction_to_comment(request, comment_id):
    """View function that handles the request for a user to add/view/change/delete reaction to a comment"""
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
        response, status = post_services.create_reaction_to_comment(request.user.id, comment_id, create_data)

    elif request.method == "GET":
        response, status = post_services.get_reactions_to_comment(request.user.id, comment_id)

    elif request.method == "DELETE":
        response, status = post_services.delete_reaction_to_comment(request.user.id, comment_id)

    else:
        return JsonResponse(data={
            "message": {
                "content": "Only POST/GET/DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)

    return JsonResponse(data=response, status=status)

@login_required(login_url="users:login")
def reference_post(request, post_id):
    """View function that handles the request for a user to reference a post"""
    pass
