from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    path("create/", views.add_post, name="add-post"),
    path("<int:post_id>/", views.view_update_delete_post, name="view-update-delete-post"),
    path("<int:post_id>/react/", views.add_update_view_delete_reaction_to_post
         , name="add-update-view-delete-reaction-to-post"),
    path("<int:post_id>/reference/", views.reference_post, name="reference-post"),
    path("compose/", views.view_post_form, name="view-post-form")
]