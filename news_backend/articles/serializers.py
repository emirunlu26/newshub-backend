from news_backend import settings

def serialize_article_teaser(article):
    if not article:
        return None

    return {
        "id": article.id,
        "slug": article.slug,
        "type": article.type,
        "title": article.title,
        "published_at": article.published_at,
        "priority_level": article.priority_level,
        "authors": [serialize_author_teaser(author) for author in article.authors],
        "summary": article.summary
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
    return {
        "article_id": article_reaction.article.id,
        "user_id": article_reaction.reaction_owner.id,
        "reaction": {
            "name": reaction_content.name,
            "icon": reaction_icon.url if reaction_icon else None
        },
        "created_at": article_reaction.created_at.strftime(settings.DATE_INPUT_FORMATS[1]),
    }