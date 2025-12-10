from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path("my-news/", views.get_my_news, name="get-my-news"),
    path("trending/", views.get_trending_articles, name="get-trending-articles"),
    path("authors/<str:slug>-<int:id>", views.get_author_by_slug_and_id, "get-author-by-slug-and-id"),
    path("<str:type>/", views.get_article_by_type(), name="get-article-by-type"),
    path("<str:type>/<str:slug>-<int:id>/", views.get_article_by_slug_and_id
         , name="get-article-by-slug-and-id"),
    path("region/<str:region>/", views.get_article_by_region, name="get-article-by-region"),
    path("category/<str:category>/", views.get_article_by_parent_category, name="get-article-by-parent-category"),
    path("category/<str:parent>/<str:sub>/", views.get_article_by_sub_category, name="get-article-by-sub-category"),
    path("tag/<str:tag>/", views.get_article_by_tag, name="get-article-by-tag")
]