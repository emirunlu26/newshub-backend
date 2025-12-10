"""View file that contains all view functions to handle requests related to articles"""
from django.shortcuts import render

# Create your views here.

def homepage(request):
    pass

def get_article_by_type(request, type):
    pass

def get_author_by_slug_and_id(request, slug, id):
    pass

def get_article_by_slug_and_id(request, type, slug, id):
    pass

def get_article_by_region(request, region):
    pass

def get_article_by_parent_category(request, parent_category):
    pass

def get_article_by_sub_category(request, parent_category, sub_category):
    pass

def get_article_by_tag(request, tag):
    pass

def get_my_news(request):
    pass

def get_trending_articles(request):
    pass
