from news_backend import settings

def serialize_article_teaser(article):
    if not article:
        return None

    return {
        "id": article.id,
        "slug": article.slug,
        "type": article.type,
        "title": article.title,
        "cover_image": article.cover_image.url if article.cover_image else None,
        "published_at": article.published_at.strftime(settings.DATE_INPUT_FORMATS[1]),
        "priority_level": article.priority_level,
        "is_premium": article.requires_premium,
        "authors": [serialize_author_teaser(author) for author in article.authors],
        "summary": article.summary,
        "trending_score": article.trending_score,
        "editorial_heat_score": article.editorial_heat_score
    }

def serialize_article(article):
    if not article:
        return None

    return {
        "id": article.id,
        "slug": article.slug,
        "type": article.type,
        "title": article.title,
        "cover_image": article.cover_image.url if article.cover_image else None,
        "published_at": article.published_at.strftime(settings.DATE_INPUT_FORMATS[1]),
        "priority_level": article.priority_level,
        "is_premium": article.requires_premium,
        "authors": [serialize_author_teaser(author) for author in article.authors],
        "tags": [serialize_tag(tag) for tag in article.tags],
        "categories": [serialize_category(category) for category in article.categories],
        "regions": [serialize_region(region) for region in article.regions],
        "content": article.content,
        "summary": article.summary,
        "trending_score": article.trending_score,
        "editorial_heat_score": article.editorial_heat_score
    }

def serialize_tag(tag):
    if not tag:
        return None
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug
    }

def serialize_category(category):
    if not category:
        return None
    parent_category = category.parent_category
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "parent_category": {
            "id": parent_category.id,
            "name": parent_category.name,
            "slug": parent_category.slug
        } if parent_category else None,
        "sub_categories": [
            {
                "id": sub_category.id,
                "name": sub_category,
                "slug": category.slug
            } for sub_category in category.sub_categories.order_by("name")
        ]
    }

def serialize_region(region):
    if not region:
        return None
    else:
        parent = region.belongs_to
        return {
            "name": region.name,
            "slug": region.slug,
            "parent_region": {
                "name": parent.name,
                "slug": parent.slug
            } if parent else None
        }

def serialize_author_teaser(author):
    if not author:
        return None
    user = author.user
    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "author_slug": author.slug,
        "about": author.about,
        "profile_image": author.profile_image.url if author.profile_image else None
    }

def serialize_article_reaction(article_reaction):
    if not article_reaction:
        return None
    reaction_content = article_reaction.reaction
    reaction_icon = reaction_content.icon
    reaction_owner = article_reaction.reaction_owner
    reaction_owner_avatar = reaction_owner.avatar
    return {
        "article_id": article_reaction.article.id,
        "user": {
            "id": reaction_owner.id,
            "username": reaction_owner.username,
            "avatar": reaction_owner_avatar.url if reaction_owner_avatar else None
        },
        "reaction": {
            "name": reaction_content.name,
            "icon": reaction_icon.url if reaction_icon else None
        },
        "created_at": article_reaction.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
    }