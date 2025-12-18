from django.urls import path, re_path
from . import views

app_name = "articles"
urlpatterns = [
    path("my-news/", views.view_my_news, name="view-my-news"),
    path("trending/", views.view_trending_articles, name="view-trending-articles"),
    path("authors/<str:slug>-<int:id>", views.view_author_by_slug_and_id, name="view-author-by-slug-and-id"),
    path("<str:type>/", views.get_articles_by_type, name="get-article-by-type"),
    re_path(r"^<str:type>/(?P<slug>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)$/", views.get_article_by_slug_and_id_with_type
         , name="get-article-by-slug-and-id-with-type"),
    re_path(r"^(?P<slug>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)$/", views.get_article_by_slug_and_id_without_type
         , name="get-article-by-slug-and-id"),
    path("region/<str:region_slug>/", views.view_articles_by_region, name="view-articles-by-region"),
    path("categories/<str:slug>/", views.view_articles_by_parent_category, name="view-articles-by-parent-category"),
    path("categories/<str:parent_slug>/<str:sub_slug>/", views.view_articles_by_sub_category
         , name="view-articles-by-sub-category"),
    path("tags/<str:slug>/", views.view_articles_by_tag, name="view-articles-by-tag"),
    path("tags/<str:slug>/follow/", views.follow_or_unfollow_tag, name="follow-or-unfollow-tag"),
    path("categories/<str:slug>/follow/", views.follow_or_unfollow_category, name="follow-or-unfollow-category"),
    path("<int:id>/bookmark/", views.bookmark_or_unbookmark_article, name="bookmark-or-unbookmark-article"),
    path("<int:id>/react", views.view_add_delete_reaction_to_article
         , name="view-add-delete-reaction-to-article")
]