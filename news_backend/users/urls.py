from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("profile/<str:username>/", views.view_profile, name="view-profile"),
    path("profile/<str:username>/photo/", views.view_profile_picture, name="view-profile-picture"),
    path("profile/<str:username>/following/", views.view_following_list, name="view-following-list"),
    path("profile/<str:username>/followers/", views.view_follower_list, name="view-follower-list"),
    path("profile/my-tags/", views.view_followed_tags, name="view-followed-tags"),
    path("profile/my-categories/", views.view_followed_categories, name="view-followed-categories"),
    path("profile/my-bookmarked-articles/", views.view_bookmarked_articles, name="view-bookmarked-articles"),
    path("settings/profile/", views.view_profile_settings, name="view-profile-settings"),
    path("settings/ui-customization/", views.view_ui_customization_settings, name="view-ui-customization-settings"),
    path("subscribe/", views.subscribe_or_unsubscribe, name="subscribe-unsubscribe"),
    path("<str:username>/follow/", views.follow_or_unfollow, name="follow-unfollow")
]