from news_backend import settings

def serialize_user_teaser(user):
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_bio": user.profile.bio,
    }

def serialize_author(author):
    user = author.user
    return {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "about": author.about,
        "profile_picture": author.profile_image.url if author.profile_image else None
    }

def serialize_ui_customization(customization):
    return {
        "username": customization.user.username,
        "theme": customization.theme,
        "font_type": customization.font_type,
        "font_size": customization.font_size,
        "font_colour": customization.font_colour
    }

def serialize_user_profile(profile):
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