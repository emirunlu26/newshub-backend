from news_backend import settings
from posts import serializers as post_serializers
from articles.serializers import serialize_article_teaser

def serialize_user_teaser(user):
    if not user:
        return None
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_bio": user.profile.bio,
    }

def serialize_author(author):
    if not author:
        return None
    user = author.user
    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "author_slug": author.slug,
        "about": author.about,
        "profile_image": author.profile_image.url if author.profile_image else None,
        "articles": [serialize_article_teaser(article) for article in author.articles.order_by("published_at")]
    }

def serialize_ui_customization(customization):
    if not customization:
        return None
    return {
        "username": customization.user.username,
        "theme": customization.theme,
        "font_type": customization.font_type,
        "font_size": customization.font_size,
        "font_colour": customization.font_colour
    }

def serialize_user_profile_settings(profile):
    if not profile:
        return None
    user = profile.user
    return {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date.strftime(settings.DATE_INPUT_FORMATS[0]),
            "gender": user.gender,
            "profile_bio": profile.bio,
            "avatar": profile.avatar.url if profile.avatar else None
        }

def serialize_user_profile(profile):
    if not profile:
        return None
    user = profile.user
    return {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birth_date": user.birth_date.strftime(settings.DATE_INPUT_FORMATS[0]),
        "gender": user.gender,
        "profile_bio": profile.bio,
        "avatar": profile.avatar.url if profile.avatar else None,
        "posts": [post_serializers.serialize_post(post) for post in user.posts]
    }