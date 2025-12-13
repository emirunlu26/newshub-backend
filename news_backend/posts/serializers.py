from news_backend import settings
from .models import PostImage

def serialize_post(post):
    owner = post.owner
    avatar = owner.avatar

    return {
        "owner": {
            "username": owner.username,
            "avatar_url": avatar.url if avatar else None
        },
        "created_at": post.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
        "updated_at": post.updated_at.strftime(settings.DATE_INPUT_FORMATS[1]),
        "referenced_article": "",
        "referenced_post": serialize_referenced_post(post.referenced_post),
        "content": post.content,
        "images": ""
    }

def serialize_referenced_post(referenced_post):
    referenced_post_owner = referenced_post.owner
    referenced_post_owner_avatar = referenced_post_owner.avatar
    post_images =
    return {
            "owner": {
                "username": referenced_post_owner.username,
                "avatar_url": referenced_post_owner_avatar.url if referenced_post_owner_avatar else None
            },
            "created_at": referenced_post.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
            "updated_at": referenced_post.updated_at.strftime(settings.DATE_INPUT_FORMATS[1]),
            "content": referenced_post.content,
            "images": ""
        }

def serialize_post_image(post_image):
    return {
        "post_id": post_image.post.id,
        "post_image_url": post_image.url,
        "rank": post_image.rank
    }