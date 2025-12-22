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
    path("profile/<str:username>/", views.get_profile, name="get-profile"),
    path("profile/<str:username>/photo/", views.get_profile_picture, name="get-profile-picture"),
    path("profile/<str:username>/following/", views.get_following_list, name="get-following-list"),
    path("profile/<str:username>/followers/", views.get_follower_list, name="get-follower-list"),
    path("profile/my-tags/", views.get_followed_tags, name="get-followed-tags"),
    path("profile/my-categories/", views.get_followed_categories, name="get-followed-categories"),
    path("profile/my-bookmarked-articles/", views.get_bookmarked_articles, name="get-bookmarked-articles"),
    path("settings/profile/", views.get_update_profile_settings, name="get-update-profile-settings"),
    path("settings/ui-customization/", views.get_update_ui_customization_settings
         , name="get-update-ui-customization-settings"),
    path("subscribe/", views.subscribe_or_unsubscribe, name="subscribe-unsubscribe"),
    path("<str:username>/follow/", views.follow_or_unfollow, name="follow-unfollow")
]