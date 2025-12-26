from models import Post

# ERROR MESSAGES
def print_comment_content_error(error_detail):
    return {
        "content": f"Invalid comment content: {error_detail}",
        "type": "error"
    }

def print_post_content_error(error_detail):
    return {
        "content": f"Invalid post content: {error_detail}",
        "type": "error"
    }


COMMENT_NOT_FOUND = {
    "content": "Comment with the given id is not found.",
    "type": "error"
}

COMMENT_CONTENT_ABSENT = {
    "content": "Data for post content is absent.",
    "type": "error",
}

COMMENT_DELETE_UNAUTHORIZED = {
    "content": "The user is not authorized to delete this comment.",
    "type": "error"
}

COMMENT_REACTION_ALREADY_CREATED = {
    "content": "This user has already reacted to this comment.",
    "type": "error"
}

PARENT_COMMENT_NOT_FOUND = {
    "content": "Parent comment with the given id is not found.",
    "type": "error"
}

POST_CONTENT_ABSENT = {
    "content": "Data for post content is absent.",
    "type": "error",
}

POST_DELETE_UNAUTHORIZED = {
    "content": "The user is not authorized to delete this post.",
    "type": "error"
}

POST_NOT_FOUND = {
    "content": "Post with the given id is not found.",
    "type": "error"
}

POST_REACTION_ALREADY_CREATED = {
    "content": "This user has already reacted to this post.",
    "type": "error"
}

POST_UPDATE_TIME_LIMIT = {
    "content": f"A post can not be updated after {Post.UPDATE_TIME_LIMIT_IN_SECONDS} seconds of its creation.",
    "type": "error"
}

POST_UPDATE_UNAUTHORIZED = {
    "content": "You're not authorized to update this post.",
    "type": "error"
}

REACTION_NAME_INVALID = {
    "content": "No name or wrong type of name for the new reaction is given.",
    "type": "error"
}

REACTION_NOT_FOUND = {
    "content": "There is no reaction defined with the given name.",
    "type": "error"
}

REFERENCED_ARTICLE_NOT_FOUND = {
    "content": "Referenced article with the given id can not be found.",
    "type": "error"
}

REFERENCED_POST_NOT_FOUND = {
    "content": "Referenced post with the given id can not be found.",
    "type": "error"
}

# SUCCESS MESSAGES
COMMENT_CREATED_SUCCESS = {
    "content": "Comment is created successfully.",
    "type": "success"
}

COMMENT_DELETED_SUCCESS = {
    "content": "Comment is created successfully.",
    "type": "success"
}

COMMENT_REACTION_DELETED_SUCCESS = {
    "content": "The reaction of the user to the comment is deleted successfully.",
    "type": "success"
}

COMMENT_REACTIONS_RETRIEVED_SUCCESS = {
    "content": "Reactions to the comment with the given id are retrieved successfully.",
    "type": "success"
}

COMMENT_REACTION_UPDATED_SUCCESS = {
    "content": "Reaction to the comment is updated successfully.",
    "type": "success"
}

COMMENT_RETRIEVED_SUCCESS = {
    "content": "Comment with the given id is retrieved successfully.",
    "type": "success"
}

POST_DELETED_SUCCESS = {
    "content": "Post is deleted successfully.",
    "type": "success"
}

POST_REACTION_CREATED_SUCCESS = {
    "content": "Reaction to the post is created successfully.",
    "type": "success"
}

POST_REACTION_DELETED_SUCCESS = {
    "content": "The reaction of the user to the post is deleted successfully.",
    "type": "success"
}

POST_REACTIONS_RETRIEVED_SUCCESS = {
    "content": "Reactions to the post with the given id are retrieved successfully.",
    "type": "success"
}

POST_RETRIEVED_SUCCESS = {
    "content": "Post with the given id is retrieved successfully.",
    "type": "success"
}

POST_UPDATED_SUCCESS = {
    "content": "Post updated successfully.",
    "type": "success"
}

# WARNING MESSAGES
COMMENT_NOT_REACTED_YET = {
    "content": "The user has already not reacted to the comment with the given id.",
    "type": "warning",
}

POST_NOT_REACTED_YET = {
    "content": "The user has already not reacted to the post with the given id.",
    "type": "warning",
}