from users.services import get_user_by_id_helper
from .models import Post, Comment
from articles.models import Article
from . import serializers as post_serializers

def get_post_by_id_helper(post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        return {
            "post": post
        }, 200
    else:
        return {
            "message": {
                "content": "Post with the given id is not found.",
                "type": "error",
                "status": 404
            },
            "post": None
        }

def get_post_by_id(post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        return {
            "message": {
                "content": "Post with the given id is retrieved successfully.",
                "type": "success",
                "status": 200
            },
            "post": post
        }
    else:
        return {
            "message": {
                "content": "Post with the given id is not found.",
                "type": "error",
                "status": 404
            }
        }

def update_post_by_id(requesting_user_id, post_id, update_data):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    post = Post.objects.filter(id=post_id).first()
    if not post:
        return {
            "messages": [
                {
                    "content": "Post with the given id can not be found.",
                    "type": "error",
                    "status": 404
                }
            ]
        }

    if post.is_created_by(requesting_user) == False:
        return {
            "messages": [
                {
                    "content": "You're not authorized to update this post.",
                    "type": "error",
                    "status": 401
                }
            ]
        }

    if post.is_update_time_over():
        return {
            "messages": [
                {
                    "content": f"You can not update a post after {Post.UPDATE_TIME_LIMIT_IN_SECONDS} seconds.",
                    "type": "error",
                    "status": 400
                }
            ]
        }

    content = update_data.get("content")
    referenced_article_id = update_data.get("referenced_article_id")
    referenced_post_id = update_data.get("referenced_article_id")

    check_dict = {
        "error_messages": [],
        "valid_update_data": {}
    }
    if content:
        content_is_valid, content_error_message = Post.is_content_valid(content)
        if content_is_valid:
            check_dict["valid_update_data"]["content"] = content
        else:
            check_dict["error_messages"].append(
                {
                    "content": f"Invalid post content: {content_error_message}",
                     "type": "error",
                    "status": 400
                }
            )
    if "referenced_article_id" in update_data:
        if not referenced_article_id:
            check_dict["valid_update_data"]["referenced_article"] = None
        else:
            article = Article.objects.filter(id=referenced_article_id).first()
            if article:
                check_dict["valid_update_data"]["referenced_article"] = article
            else:
                check_dict["error_messages"].append(
                    {
                        "content": "Article with the given id to reference can not be found.",
                        "type": "error",
                        "status": 404
                    }
                )

    if "referenced_post_id" in update_data:
        if not referenced_post_id:
            check_dict["valid_update_data"]["referenced_post"] = None
        else:
            post = Post.objects.filter(id=referenced_post_id).first()
            if post:
                check_dict["valid_update_data"]["referenced_post"] = post
            else:
                check_dict["error_messages"].append(
                    {
                        "content": "Post with the given id to reference can not be found.",
                        "type": "error",
                        "status": 404
                    }
                )
    # If there is any error, return all error messages. Otherwise, update data with the validated data.
    if check_dict["error_messages"]:
        return {
            "messages": check_dict["error_messages"]
        }
    else:
        if "content" in check_dict["valid_update_data"]:
            post.content = check_dict["valid_update_data"]["content"]

        if "referenced_article" in check_dict["valid_update_data"]:
            post.referenced_article = check_dict["valid_update_data"]["referenced_article"]

        if "referenced_post" in check_dict["valid_update_data"]:
            post.referenced_post = check_dict["valid_update_data"]["referenced_post"]

        # Save updates
        post.save()

        return {
            "messages": [
                {
                    "content": "Post updated successfully.",
                    "type": "success",
                    "status": 200
                }
            ]
        }

def delete_post_by_id(requesting_user_id, post_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    post = Post.objects.filter(id=post_id).first()
    if not post:
        return {
            "message": {
                "content": "Post with the given id can not be found.",
                "type": "error",
                "status": 404
            }
        }

    if requesting_user.is_superuser or post.is_created_by(requesting_user):
        post.delete()
        return {
            "message": {
                "content": "Post is deleted successfully.",
                "type": "success",
                "status": 200
            }
        }
    else:
        return {
            "message": {
                "content": "You're not authorized to delete this post.",
                "type": "error",
                "status": 401
            }
        }

def get_comment_by_id(comment_id):
    comment = Comment.objects.filter(id=comment_id).first()

    if comment:
        return {
            "message": {
                "content": "Comment with the given id is retrieved successfully.",
                "type": "success",
                "status": 200
            },
            "comment": post_serializers.serialize_comment(comment)
        }
    else:
        return {
            "message": {
                "content": "Comment with the given id can not be found.",
                "type": "error",
                "status": 404
            },
        }

def create_comment(user_id, post_id, create_data):
    response = get_user_by_id_helper(user_id)
    if not response["user"]:
        return response
    user = response["user"]

    response = get_post_by_id_helper(post_id)
    if not response["post"]:
        return response
    post = response["post"]

    parent_comment_id = create_data.get("parent_comment_id")
    content = create_data.get("content")

    if not content:
        return {
            "message": {
                "content": "There is not content given for the comment to be created.",
                "type": "error",
                "status": 400
            }
        }

    # if parent_comment_id is provided, check its existence, else assume that there is no parent_comment
    parent_comment = None
    if parent_comment_id:
        parent_comment = Comment.objects.filter(id=parent_comment_id).first()
        if not parent_comment:
            return {
                "message": {
                    "content": "There is no parent comment with the given id.",
                    "type": "error",
                    "status": 404
                }
            }

    content_valid, content_error_message = Comment.is_content_valid(content)
    if not content_valid:
        return {
            "message": {
                "content": f"Invalid comment content: {content_error_message}",
                "type": "error",
                "status": 400
            }
        }

    new_comment = Comment.objects.create(
        owner=user,
        post=post,
        content=content,
        parent_comment=parent_comment
    )
    new_comment.save()

    return {
        "message": {
            "content": "Comment created successfully.",
            "type": "success",
            "status": 200
        },
        "comment": post_serializers.serialize_comment(new_comment)
    }

def delete_comment_by_id(requesting_user_id, comment_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    comment = Comment.objects.filter(id=comment_id).first()
    if not comment:
        return {
            "message": {
                "content": "There is no comment with the given id.",
                "type": "error",
                "status": 404
            }
        }

    if requesting_user.is_superuser or comment.is_created_by(requesting_user):
        comment.delete()
        return {
            "message": {
                "content": "Comment is deleted successfully.",
                "type": "success",
                "status": 200
            }
        }
    else:
        return {
            "message": {
                "content": "You're not authorized to delete this comment.",
                "type": "error",
                "status": 401
            }
        }


