from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("posts/create/", views.create_post, name="create-post"),
    path("posts/<int:post_id>/comments/create/", views.create_comment, name="create-comment"),
    path("posts/<int:post_id>/", views.get_update_delete_post, name="get-update-delete-post"),
    path("comments/<int:comment_id>", views.get_delete_comment, name="get-delete-comment"),
    path("posts/<int:post_id>/react/", views.create_get_delete_reaction_to_post
         , name="create-get-delete-reaction-to-post"),
    path("comments/<int:comment_id>/react", views.create_get_delete_reaction_to_comment
         , name="create-get-delete-reaction-to-comment"),
    path("posts/<int:post_id>/reference/", views.reference_post, name="reference-post"),
]