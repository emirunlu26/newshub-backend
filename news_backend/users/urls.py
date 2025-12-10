from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("password_change/", auth_views.PasswordChangeView.as_view()),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view()),
    path("password_reset/", auth_views.PasswordResetView.as_view()),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view()),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view()),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view()),
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