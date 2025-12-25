"""View file that contains all view functions to handle requests related to articles"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from . models import Article
from . import services
import json

# Create your views here.

def homepage(request):
    # TO DO: Implement homepage view
    pass

def get_trending_articles(request):
    if request.method == "GET":
        response = services.get_trending_articles()
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_articles_by_type(request, type):
    if request.method == "GET":
        response = services.get_articles_by_type(type)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_slug_and_id(request, slug, id):
    if request.method == "GET":
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        response = services.get_article_by_slug_and_id(request.user.id, session_id, slug, id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_articles_by_region(request, region_slug):
    if request.method == "GET":
        response = services.get_articles_by_region(request.user.id, region_slug)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_articles_by_parent_category(request, slug):
    if request.method == "GET":
        response = services.get_articles_by_parent_category(request.user.id, slug)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_articles_by_sub_category(request, parent_slug, sub_slug):
    if request.method == "GET":
        response = services.get_articles_by_sub_category(request.user.id, parent_slug, sub_slug)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_articles_by_tag(request, slug):
    if request.method == "GET":
        response = services.get_articles_by_tag(request.user.id, slug)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_author_by_slug_and_id(request, slug, id):
    if request.method == "GET":
        response = services.get_author_by_slug_and_id(slug, id)
        return JsonResponse(data=response, status=response["message"]["status"])
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_my_news(request):
    # TO DO: Implement get_my_news view
    pass

@login_required(login_url="users:login")
def get_add_delete_reaction_to_article(request, article_id):
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
        response = services.create_reaction_to_article(request.user.id, article_id, create_data)
        return JsonResponse(data=response, status=response["message"]["status"])

    elif request.method == "GET":
        response = services.get_reactions_to_article(request.user.id, article_id)
        return JsonResponse(data=response, status=response["message"]["status"])

    elif request.method == "DELETE":
        response = services.delete_reaction_to_article(request.user.id, article_id)
        return JsonResponse(data=response, status=response["message"]["status"])

    else:
        return JsonResponse(data={
            "message": {
                "content": "Only POST/GET/DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def follow_or_unfollow_tag(request, slug):
    if request.method == "POST":
        response = services.follow_tag(request.user.id, slug)
    elif request.method == "DELETE":
        response = services.unfollow_tag(request.user.id, slug)
    else:
        return JsonResponse(data={
            "message": {
                "content": "Only POST and DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=response["message"]["status"])

@login_required(login_url="users:login")
def follow_or_unfollow_category(request, slug):
    if request.method == "POST":
        response = services.follow_category(request.user.id, slug)
    elif request.method == "DELETE":
        response = services.unfollow_category(request.user.id, slug)
    else:
        return JsonResponse(data={
            "message": {
                "content": "Only POST and DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=response["message"]["status"])

@login_required(login_url="users:login")
def bookmark_or_unbookmark_article(request, id):
    if request.method == "POST":
        response = services.bookmark_article(request.user.id, id)
    elif request.method == "DELETE":
        response = services.unbookmark_article(request.user.id, id)
    else:
        return JsonResponse(data={
            "message": {
                "content": "Only POST and DELETE requests are allowed.",
                "type": "error"
            }
        }, status=405)
    return JsonResponse(data=response, status=response["message"]["status"])
