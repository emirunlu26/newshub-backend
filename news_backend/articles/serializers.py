def serialize_article_teaser(article):
    if not article:
        return None

    return {
        "id": article.id,
        "slug": article.slug,
        "type": article.type,
        "title": article.title,
        "authors": [serialize_author(author) for author in article.authors],
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
        } if parent_category else None
    }

def serialize_author(author):
    if not author:
        return None
    user = author.user
    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "about": author.about,
        "profile_picture": author.profile_image.url if author.profile_image else None
    }