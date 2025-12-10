from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("posts/create/", views.add_post, name="add-post"),
    path("posts/<int:post_id>/comments/create/", views.add_comment, name="add-comment"),
    path("posts/<int:post_id>/", views.view_update_delete_post, name="view-update-delete-post"),
    path("comments/<int:comment_id>", views.view_update_delete_comment, name="view-update-delete-comment"),
    path("posts/<int:post_id>/react/", views.view_add_update_delete_reaction_to_post
         , name="add-update-view-delete-reaction-to-post"),
    path("comments/<int:comment_id>/react", views.view_add_update_delete_reaction_to_comment
         , name="add-update-view-delete-reaction-to-post"),
    path("posts/<int:post_id>/reference/", views.reference_post, name="reference-post"),
]