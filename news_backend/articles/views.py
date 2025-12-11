"""View file that contains all view functions to handle requests related to articles"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from . models import Article
import json

# Create your views here.

def homepage(request):
    pass

@login_required(login_url="users:login")
def create_article(request):
    pass

@login_required(login_url="users:login")
def update_or_delete_article(request, id):
    pass

@login_required(login_url="users:login")
def get_articles_by_type(request, type):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_slug_and_id_with_type(request, type, slug, id):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_slug_and_id_without_type(request, slug, id):
    if request.method == "GET":
        try:
            register_data = json.loads(request.body)
        except:
            return JsonResponse(data={
                "message": {
                    "content": "Invalid JSON.",
                    "type": "error"
                }
            }, status=400)
        article = Article.objects.filter(id=id, slug=slug).first()
        if article is None:
            return JsonResponse(data={
                "message": {
                    "content": "Article not found, id and/or slug does not match.",
                    "type": "error"
                }
            }, status=404)
        else:
            return redirect(
                to="get-article-by-slug-and-id-with-type",
                type=article.type,
                slug=slug,
                id=id
            )
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_region(request, region):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_parent_category(request, slug):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_sub_category(request, parent_slug, sub_slug):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_article_by_tag(request, slug):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_author_by_slug_and_id(request, slug, id):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def get_my_news(request):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

def get_trending_articles(request):
    if request.method == "GET":
        pass
    else:
        return JsonResponse(data={
            "message": {
                "content": "GET request required.",
                "type": "error"
            }
        }, status=405)

@login_required(login_url="users:login")
def follow_or_unfollow_tag(request, slug):
    pass

@login_required(login_url="users:login")
def follow_or_unfollow_category(request, slug):
    pass

@login_required(login_url="users:login")
def bookmark_or_unbookmark_article(request, id):
    pass

@login_required(login_url="users:login")
def view_add_update_delete_reaction_to_article(request, post_id):
    pass
