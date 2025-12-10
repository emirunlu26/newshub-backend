"""View file that contains all view functions to handle requests related to articles"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
    pass

def get_article_by_slug_and_id_with_type(request, type, slug, id):
    pass

def get_article_by_slug_and_id_without_type(request, slug, id):
    pass

def get_article_by_region(request, region):
    pass

def get_article_by_parent_category(request, slug):
    pass

def get_article_by_sub_category(request, parent_slug, sub_slug):
    pass

def get_article_by_tag(request, slug):
    pass

def get_author_by_slug_and_id(request, slug, id):
    pass

@login_required(login_url="users:login")
def get_my_news(request):
    pass

def get_trending_articles(request):
    pass

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
