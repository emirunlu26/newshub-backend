from users.services import get_user_by_id_helper
from models import Tag, Category

def get_tag_by_slug_helper(tag_slug):
    tag = Tag.objects.filter(slug=tag_slug).first()
    if tag:
        return {
            "tag": tag
        }
    else:
        return {
            "message": {
                "content": "Tag with the given slug can not be found.",
                "type": "error",
                "status": 404
            },
            "tag": None
        }

def get_category_by_slug_helper(category_slug):
    category = Category.objects.filter(slug=category_slug).first()
    if category:
        return {
            "category": category
        }
    else:
        return {
            "message": {
                "content": "Category with the given slug can not be found.",
                "type": "error",
                "status": 404
            },
            "category": None
        }

def follow_tag(requesting_user_id, tag_slug):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_tag_by_slug_helper(tag_slug)
    if not response["tag"]:
        return response

    tag = response["tag"]

    tag_followed = requesting_user.followed_tags.filter(tag=tag).exists()
    if tag_followed:
        return {
            "message": {
                "content": "This user already follows the tag with the given slug.",
                "type": "warning",
                "status": 200
            }
        }

    requesting_user.followed_tags.add(tag)

    return {
        "message": {
            "content": "Tag with the given slug is followed successfully.",
            "type": "success",
            "status": 200
        }
    }

def unfollow_tag(requesting_user_id, tag_slug):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_tag_by_slug_helper(tag_slug)
    if not response["tag"]:
        return response

    tag = response["tag"]

    tag_followed = requesting_user.followed_tags.filter(tag=tag).exists()
    if not tag_followed:
        return {
            "message": {
                "content": "This user already does not follow the tag with the given slug.",
                "type": "warning",
                "status": 200
            }
        }

    requesting_user.followed_tags.remove(tag)

    return {
        "message": {
            "content": "Tag with the given slug is unfollowed successfully.",
            "type": "success",
            "status": 200
        }
    }

def follow_category(requesting_user_id, category_slug):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_category_by_slug_helper(category_slug)
    if not response["category"]:
        return response

    category = response["category"]

    category_followed = requesting_user.followed_categories.filter(category=category).exists()
    if category_followed:
        return {
            "message": {
                "content": "This user already follows the category with the given slug.",
                "type": "warning",
                "status": 200
            }
        }

    requesting_user.followed_categories.add(category)

    return {
        "message": {
            "content": "Category with the given slug is followed successfully.",
            "type": "success",
            "status": 200
        }
    }

def unfollow_category(requesting_user_id, category_slug):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_category_by_slug_helper(category_slug)
    if not response["category"]:
        return response

    category = response["category"]

    category_followed = requesting_user.followed_categories.filter(category=category).exists()
    if not category_followed:
        return {
            "message": {
                "content": "This user already does not follow the category with the given slug.",
                "type": "warning",
                "status": 200
            }
        }

    requesting_user.followed_categories.remove(category)

    return {
        "message": {
            "content": "Category with the given slug is unfollowed successfully.",
            "type": "success",
            "status": 200
        }
    }