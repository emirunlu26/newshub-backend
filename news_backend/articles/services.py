from users.services import get_user_by_id_helper
from users.models import Author
from users import serializers as user_serializers
from articles import serializers as article_serializers
from articles.models import Tag, Category, Article, Region, ArticleReaction, ArticleView
from articles import messages
from posts.models import Reaction

def get_tag_by_slug_helper(tag_slug):
    tag = Tag.objects.filter(slug=tag_slug).first()
    if tag:
        return {
            "tag": tag
        }
    else:
        return {
            "message": messages.TAG_NOT_FOUND,
            "tag": None
        }, 404

def get_category_by_slug_helper(category_slug):
    category = Category.objects.filter(slug=category_slug).first()
    if category:
        return {
            "category": category
        }
    else:
        return {
            "message": messages.CATEGORY_NOT_FOUND,
            "category": None
        }, 404

def get_published_article_by_id_helper(id):
    article = Article.objects.filter(id=id, published_at__isnull=False).first()
    if article:
        return {"article": article}
    else:
        return {
            "message": messages.PUBLISHED_ARTICLE_ID_NOT_FOUND,
            "article": None
        }, 404

def get_article_by_slug_and_id(requesting_user_id, session_id, article_slug, article_id):
    requesting_user = None
    if requesting_user_id:
        response = get_user_by_id_helper(requesting_user_id)
        if not response["user"]:
            return response
        requesting_user = response["user"]

    article = (Article.objects
               .filter(slug=article_slug, id=article_id, published_at__isnull=False)
               .first())

    if not article:
        return {"message": messages.PUBLISHED_ARTICLE_ID_SLUG_NOT_FOUND}, 404

    if article.requires_premium and (not requesting_user or not requesting_user.profile.is_premium()):
        return {"message": messages.PREMIUM_ARTICLE_UNAUTHORIZED_ACCESS}, 401

    # Register the view of the article
    if requesting_user:
        ArticleView.objects.create(user=requesting_user, article=article)
    else:
        ArticleView.objects.create(session_id=session_id, article=article)

    return {
        "message": messages.ARTICLE_RETRIEVED_SUCCESS,
        "article": article_serializers.serialize_article(article),
        "is_bookmarked": requesting_user.bookmarked_articles.filter(article=article).exists()
        if requesting_user else False
    }, 200


def get_author_by_slug_and_id(slug, id):
    author = Author.objects.filter(id=id, slug=slug).first()
    if not author:
        return {"message": messages.AUTHOR_NOT_FOUND}, 404
    else:
        return {
            "message": messages.AUTHOR_RETRIEVED_SUCCESS,
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
        sub_categories = category.get_all_sub_categories()
        sub_category_slugs = [sub_category.slug for sub_category in sub_categories]
        published_articles_of_category = (Article.objects
                                          .filter(published_at__isnull=False, categories__slug__in=sub_category_slugs)
                                          .distinct())
        TOP_K = 20
        EDITORIAL_HEAT_ORDER = "-editorial_heat_score"
        sorted_articles = (published_articles_of_category
                           .filter(editorial_heat_score__gt=0)
                           .order_by(EDITORIAL_HEAT_ORDER))[:TOP_K]

        return {
            "message": messages.ARTICLES_OF_PARENT_CATEGORY_RETRIEVED_SUCCESS,
            "articles": [article_serializers.serialize_article_teaser(article) for article in sorted_articles],
            "category": article_serializers.serialize_category(category),
            "category_followed": requesting_user.followed_categories.filter(slug=category_slug).exists()
            if requesting_user else False
        }, 200
    else:
        return {
            "message": messages.NOT_PARENT_CATEGORY,
            "redirect_to": f"/articles/categories/{category.parent_category.slug}/{category.slug}"
        }, 301

def get_articles_by_sub_category(requesting_user_id, parent_slug, sub_slug):
    requesting_user = None
    if requesting_user_id:
        response = get_user_by_id_helper(requesting_user_id)
        if not response["user"]:
            return response
        requesting_user = response["user"]

    parent_category = Category.objects.filter(slug=parent_slug, parent_category__isnull=True)
    if not parent_category:
        return {"message": messages.PARENT_CATEGORY_NOT_FOUND}, 404

    sub_category = Category.objects.filter(slug=sub_slug, parent_category__isnull=False)
    if not sub_category:
        return {"message": messages.SUB_CATEGORY_NOT_FOUND}, 404

    if sub_category.parent_category.slug != parent_slug:
        return {"message": messages.PARENT_CATEGORY_NOT_MATCHED}, 400

    published_articles_of_category = Article.objects.filter(published_at__isnull=False, categories__slug=sub_slug)

    TOP_K = 10
    EDITORIAL_HEAT_ORDER = "-editorial_heat_score"
    sorted_articles = (published_articles_of_category
                       .filter(editorial_heat_score__gt=0)
                       .order_by(EDITORIAL_HEAT_ORDER))[:TOP_K]

    return {
        "message": messages.ARTICLES_OF_SUB_CATEGORY_RETRIEVED_SUCCESS,
        "articles": [article_serializers.serialize_article_teaser(article) for article in sorted_articles],
        "parent_category": article_serializers.serialize_category(parent_category),
        "sub_category": article_serializers.serialize_category(sub_category),
        "category_followed": requesting_user.followed_categories.filter(slug=sub_slug).exists()
        if requesting_user else False
    }, 200

def get_articles_by_region(requesting_user_id, region_slug):
    requesting_user = None
    if requesting_user_id:
        response = get_user_by_id_helper(requesting_user_id)
        if not response["user"]:
            return response
        requesting_user = response["user"]

    region = Region.objects.filter(slug=region_slug).first()
    if not region:
        return {"message": messages.REGION_NOT_FOUND}, 404

    regions_to_search = [region] + region.get_all_sub_regions()
    region_slugs_to_search = [region.slug for region in regions_to_search]

    published_articles_of_region = (Article.objects
                .filter(regions__slug__in=region_slugs_to_search, published_at__isnull=False)
                .distinct())

    TOP_K = 20
    EDITORIAL_HEAT_ORDER = "-editorial_heat_score"
    sorted_articles = (published_articles_of_region
                       .filter(editorial_heat_score__gt=0)
                       .order_by(EDITORIAL_HEAT_ORDER))[:TOP_K]

    return {
        "message": messages.ARTICLES_OF_REGION_RETRIEVED_SUCCESS,
        "articles": [article_serializers.serialize_article_teaser(article) for article in sorted_articles],
        "region": article_serializers.serialize_region(region)
    }, 200

def get_articles_by_type(article_type):
    valid_article_types = [article_type_choice[0] for article_type_choice in Article.ARTICLE_TYPE_CHOICES]

    if type(article_type) != str:
        return {"message": messages.ARTICLE_TYPE_INVALID_FORMAT}, 400

    if article_type not in valid_article_types:
        return {"message": messages.ARTICLE_TYPE_NOT_FOUND}, 404

    articles = Article.objects.filter(type=article_type, published_at__isnull=False).order_by("-created_at")

    return {
        "message": messages.ARTICLES_OF_SAME_TYPE_RETRIEVED_SUCCESS,
        "articles": [article_serializers.serialize_article_teaser(article) for article in articles]
    }, 200

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
    articles = (Article.objects
                .filter(tags__slug=tag_slug, published_at__isnull=False)
                .order_by(ARTICLE_ORDER))

    return {
        "message": messages.ARTICLES_WITH_GIVEN_TAG_RETRIEVED_SUCCESS,
        "articles": [article_serializers.serialize_article_teaser(article) for article in articles],
        "tag": article_serializers.serialize_tag(tag),
        "tag_followed": requesting_user.followed_tags.filter(slug=tag_slug).exists() if requesting_user else False
    }, 200


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
        return {"message": messages.TAG_ALREADY_FOLLOWED}, 200

    requesting_user.followed_tags.add(tag)

    return {"message": messages.TAG_FOLLOWED_SUCCESS}, 200

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
        return {"message": messages.TAG_NOT_FOLLOWED_YET}, 200

    requesting_user.followed_tags.remove(tag)

    return {"message": messages.TAG_UNFOLLOWED_SUCCESS}, 200

def follow_category(requesting_user_id, category_slug):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    response = get_category_by_slug_helper(category_slug)
    if not response["category"]:
        return response
    category = response["category"]

    # If the category is a parent category ...
    if not category.parent_category:
        slugs_of_already_followed_sub_categories = [
            category.slug for category in requesting_user.followed_categories.filter(parent_category=category)
        ]
        not_followed_sub_categories = (Category.objects
                          .filter(parent_category=category)
                          .exclude(slug__in=slugs_of_already_followed_sub_categories))
        requesting_user.followed_categories.add(*not_followed_sub_categories)

        return {"message": messages.PARENT_CATEGORY_FOLLOWED_SUCCESS}, 200

    else:
        category_followed = requesting_user.followed_categories.filter(category=category).exists()
        if category_followed:
            return {"message": messages.CATEGORY_ALREADY_FOLLOWED}, 200

        requesting_user.followed_categories.add(category)

        return {"message": messages.SUB_CATEGORY_FOLLOWED_SUCCESS}, 200

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
        return {"message": messages.CATEGORY_NOT_FOLLOWED_YET}, 200

    requesting_user.followed_categories.remove(category)

    return {
        "message": {
            "content": "Category with the given slug is unfollowed successfully.",
            "type": "success",
        }
    }, 200

def bookmark_article(requesting_user_id, article_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_published_article_by_id_helper(article_id)
    if not response["article"]:
        return response

    article = response["article"]

    if article.requires_premium and (requesting_user.profile.is_premium() == False):
        return {"message": messages.PREMIUM_ARTICLE_BOOKMARK_UNAUTHORIZED}, 401

    article_bookmarked = requesting_user.bookmarked_articles.filter(article=article).exists()
    if article_bookmarked:
        return {"message": messages.ARTICLE_ALREADY_BOOKMARKED}, 200

    requesting_user.bookmarked_articles.add(article)

    return {"message": messages.ARTICLE_BOOKMARKED_SUCCESS}, 200

def unbookmark_article(requesting_user_id, article_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response

    requesting_user = response["user"]

    response = get_published_article_by_id_helper(article_id)
    if not response["article"]:
        return response

    article = response["article"]

    article_bookmarked = requesting_user.bookmarked_articles.filter(article=article).exists()
    if not article_bookmarked:
        return {"message": messages.ARTICLE_NOT_YET_BOOKMARKED}, 200

    requesting_user.bookmarked_articles.remove(article)

    return {"message": messages.ARTICLE_UNBOOKMARKED_SUCCESS}, 200

def create_reaction_to_article(requesting_user_id, article_id, create_data):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    response = get_published_article_by_id_helper(article_id)
    if not response["article"]:
        return response
    article_to_react = response["article"]

    if article_to_react.requires_premium and not requesting_user.profile.is_premium():
        return {"message": messages.PREMIUM_ARTICLE_REACT_UNAUTHORIZED}, 401

    already_reacted = ArticleReaction.objects.filter(reaction_owner=requesting_user, article=article_to_react).exists()
    if already_reacted:
        return {"message": messages.ARTICLE_ALREADY_REACTED}, 409

    new_reaction_name = create_data.get("new_reaction_name")

    if not new_reaction_name or not type(new_reaction_name) is str:
        return {"message": messages.INVALID_REACTION_NAME}, 400

    new_reaction_content = Reaction.objects.filter(name=new_reaction_name).first()
    if not new_reaction_content:
        return {"message": messages.REACTION_NOT_FOUND}, 404

    new_article_reaction = ArticleReaction.objects.create(
        article=article_to_react,
        reaction=new_reaction_content,
        reaction_owner=requesting_user
    )

    return {
        "message": messages.ARTICLE_REACTION_CREATED_SUCCESS,
        "article_reaction": article_serializers.serialize_article_reaction(new_article_reaction)
    }, 200

def get_reactions_to_article(requesting_user_id, article_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    response = get_published_article_by_id_helper(article_id)
    if not response["article"]:
        return response
    reacted_article = response["article"]

    sorted_reactions = ArticleReaction.get_sorted_reactions(requesting_user, reacted_article)

    return {
        "message": messages.ARTICLE_REACTIONS_RETRIEVED_SUCCESS,
        "reactions": [article_serializers.serialize_article_reaction(reaction) for reaction in sorted_reactions]
    }, 200

def delete_reaction_to_article(requesting_user_id, article_id):
    response = get_user_by_id_helper(requesting_user_id)
    if not response["user"]:
        return response
    requesting_user = response["user"]

    response = get_published_article_by_id_helper(article_id)
    if not response["article"]:
        return response
    reacted_article = response["article"]

    article_reaction = ArticleReaction.objects.filter(reaction_owner=requesting_user, article=reacted_article).first()

    if not article_reaction:
        return {"message": messages.ATTEMPT_TO_DELETE_NON_EXISTENT_ARTICLE_REACTION}, 200

    article_reaction.delete()

    return {"message": messages.ARTICLE_REACTION_DELETED_SUCCESS}, 200

def get_trending_articles():
    TRENDING_ORDER = "-trending_score"
    TOP_K = 20
    trending_articles = Article.objects.filter(trending_score__gt=0).order_by(TRENDING_ORDER)[:TOP_K]

    return {
        "message": messages.TRENDING_ARTICLES_RETRIEVED_SUCCESS,
        "articles": [article_serializers.serialize_article_teaser(article) for article in trending_articles]
    }, 200
