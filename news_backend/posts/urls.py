from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("posts/create/", views.create_post, name="create-post"),
    path("posts/<int:post_id>/comments/create/", views.create_comment, name="create-comment"),
    path("posts/<int:post_id>/", views.view_update_delete_post, name="view-update-delete-post"),
    path("comments/<int:comment_id>", views.view_delete_comment, name="view-delete-comment"),
    path("posts/<int:post_id>/react/", views.create_view_delete_reaction_to_post
         , name="create-view-delete-reaction-to-post"),
    path("comments/<int:comment_id>/react", views.create_view_delete_reaction_to_comment
         , name="create-view-delete-reaction-to-comment"),
    path("posts/<int:post_id>/reference/", views.reference_post, name="reference-post"),
]