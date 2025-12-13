from users.services import get_user_by_id
from .models import Post, Comment
from .serializers import serialize_post, serialize_comment

def get_post_by_id(post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        return {
            "post": post
        }, 200
    else:
        return {
            "message": {
                "content": "Post with the given id is not found.",
                "type": "error"
            },
            "post": None
        }, 404
def create_comment(user_id, post_id, create_data):
    response, status = get_user_by_id(user_id)
    if not response["user"]:
        return response, status
    user = response["user"]

    response, status = get_post_by_id(post_id)
    if not response["post"]:
        return response, status
    post = response["post"]

    parent_comment_id = create_data.get("parent_comment_id")
    content = create_data.get("content")

    if not content:
        return {
            "message": {
                "content": "There is not content given for the comment to be created.",
                "type": "error"
            }
        }, 400

    # if parent_comment_id is provided, check its existence, else assume that there is no parent_comment
    parent_comment = None
    if parent_comment_id:
        parent_comment = Comment.objects.filter(id=parent_comment_id)
        if not parent_comment:
            return {
                "message": {
                    "content": "There is no parent comment with the given id.",
                    "type": "error"
                }
            }, 404

    content_valid, content_error_message = Comment.is_content_valid(content)
    if not content_valid:
        return {
            "message": {
                "content": f"Invalid comment content: {content_error_message}",
                "type": "error"
            }
        }, 400

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
            "type": "success"
        },
        "comment": serialize_comment(new_comment)
    }


