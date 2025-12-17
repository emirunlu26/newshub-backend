from django.shortcuts import redirect
from users.services import get_user_by_id_helper
from users.models import Author
from users import serializers as user_serializers
from articles import serializers as article_serializers
from articles.models import Tag, Category, Article

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

def get_article_by_id_helper(id):
    article = Article.objects.filter(id=id).first()
    if article:
        return {"article": article}
    else:
        return {
            "message": {
                "content": "Article with the given id can not be found.",
                "type": "error",
                "status": 404
            },
            "article": None
        }

def get_author_by_slug_and_id(slug, id):
    author = Author.objects.filter(id=id, slug=slug).first()
    if not author:
        return {
            "message": {
                "content": "Author with the given id and slug can not be found.",
                "type": "error",
                "status": 404
            }
        }
    else:
        return {
            "message": {
                "content": "Author with the given id and slug is retrieved successfully.",
                "type": "success",
                "status": 200
            },
            "author": user_serializers.serialize_author(author)
        }

def get_articles_by_parent_category(requesting_user_id, category_slug):
    requesting_user = None
    if requesting_user_id:
        response = get_user_by_id_helper(requesting_user_id)
        if not response["user"]:
            return response
        requesting_user = response["user"]

    response = get_category_by_slug_helper(category_slug)
    if not response["category"]:
        return response
    category = response["category"]

    is_parent = not category.parent_category
    if is_parent:
        sorted_articles = (
            Article.get_sorted_articles_of_same_category(requesting_user_id, category_slug, is_parent=True)
                           )
        return {
            "message": {
                "content": "All articles with the given parent category are sorted and retrieved successfully.",
                "type": "success",
                "status": 200
            },
            "articles": [article_serializers.serialize_article_teaser(article) for article in sorted_articles],
            "category": article_serializers.serialize_category(category),
            "category_followed": requesting_user.followed_categories.filter(slug=category_slug).exists()
            if requesting_user else False
        }
    else:
        return redirect(
            to="view-articles-by-sub-category",
            parent_slug= category.parent_category.slug,
            sub_slug= category_slug
        )



def get_articles_by_tag(requesting_user_id, tag_slug):
    requesting_user = None
    if requesting_user_id:
        response = get_user_by_id_helper(requesting_user_id)
        if not response["user"]:
            return response
        requesting_user = response["user"]

    response = get_tag_by_slug_helper(tag_slug)
    if not response["tag"]:
        return response
    tag = response["tag"]

    ARTICLE_ORDER = "-published_at"
    articles = Article.objects.filter(tags__slug=tag_slug).filter(status="published").order_by(ARTICLE_ORDER)

    return {
        "message": {
            "content": "Articles having the tag with the given slug are retrieved successfully.",
            "type": "success",
            "status": 200
        },
        "articles": [article_serializers.serialize_article_teaser(article) for article in articles],
        "tag": article_serializers.serialize_tag(tag),
        "tag_followed": requesting_user.followed_tags.filter(slug=tag_slug).exists() if requesting_user else False
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

def bookmark_article(requesting_user_id, article_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_article_by_id_helper(article_id)
    if not response["article"]:
        return response

    article = response["article"]

    if article.requires_premium and (requesting_user.profile.is_premium() == False):
        return {
            "message": {
                "content": "A user with a non-premium profile can not bookmark a premium-only article.",
                "type": "error",
                "status": 401
            }
        }

    article_bookmarked = requesting_user.bookmarked_articles.filter(article=article).exists()
    if article_bookmarked:
        return {
            "message": {
                "content": "This user already bookmarked the article with the given id.",
                "type": "warning",
                "status": 200
            }
        }

    requesting_user.bookmarked_articles.add(article)

    return {
        "message": {
            "content": "The article with the given id is bookmarked successfully.",
            "type": "success",
            "status": 200
        }
    }

def unbookmark_article(requesting_user_id, article_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_article_by_id_helper(article_id)
    if not response["article"]:
        return response

    article = response["article"]

    article_bookmarked = requesting_user.bookmarked_articles.filter(article=article).exists()
    if not article_bookmarked:
        return {
            "message": {
                "content": "This user already did not bookmark the article with the given id.",
                "type": "warning",
                "status": 200
            }
        }

    requesting_user.bookmarked_articles.remove(article)

    return {
        "message": {
            "content": "The article with the given id is unbookmarked successfully.",
            "type": "success",
            "status": 200
        }
    }
