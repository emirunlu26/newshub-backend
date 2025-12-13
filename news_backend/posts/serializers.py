from news_backend import settings
from articles import serializers as article_serializers
from .models import PostImage

def serialize_post(post):
    if not post:
        return None
    owner = post.owner
    avatar = owner.avatar

    return {
        "owner": {
            "username": owner.username,
            "avatar_url": avatar.url if avatar else None
        },
        "created_at": post.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
        "updated_at": post.updated_at.strftime(settings.DATE_INPUT_FORMATS[1]),
        "referenced_article": article_serializers.serialize_article_teaser(post.referenced_article),
        "referenced_post": serialize_referenced_post(post.referenced_post),
        "content": post.content,
        "images": [serialize_post_image(post_image) for post_image in post.images.order_by("rank")]
    }

def serialize_referenced_post(referenced_post):
    if not referenced_post:
        return None
    referenced_post_owner = referenced_post.owner
    referenced_post_owner_avatar = referenced_post_owner.avatar
    return {
            "owner": {
                "username": referenced_post_owner.username,
                "avatar_url": referenced_post_owner_avatar.url if referenced_post_owner_avatar else None
            },
            "created_at": referenced_post.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
            "updated_at": referenced_post.updated_at.strftime(settings.DATE_INPUT_FORMATS[1]),
            "content": referenced_post.content,
            "images": [serialize_post_image(post_image) for post_image in referenced_post.images.order_by("rank")]
        }

def serialize_post_image(post_image):
    if not post_image:
        return None
    return {
        "post_id": post_image.post.id,
        "id": post_image.id,
        "url": post_image.url,
        "rank": post_image.rank
    }

def serialize_comment(comment, include_parent=True):
    if not comment:
        return None
    owner = comment.owner
    owner_avatar = owner.avatar
    if include_parent:
        parent_comment = comment.parent_comment
        return {
            "owner": {
                "username": owner.username,
                "avatar_url": owner_avatar.url if owner_avatar else None
            },
            "post_id": comment.post.id,
            "content": comment.content,
            "parent_comment": serialize_comment(parent_comment, include_parent=False) if parent_comment else None,
            "created_at": comment.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
            "updated_at": comment.updated_at.strftime(settings.DATE_INPUT_FORMATS[1])
        }
    else:
        return {
            "owner": {
                "username": owner.username,
                "avatar_url": owner_avatar.url if owner_avatar else None
            },
            "post_id": comment.post.id,
            "content": comment.content,
            "created_at": comment.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
            "updated_at": comment.updated_at.strftime(settings.DATE_INPUT_FORMATS[1])
        }
