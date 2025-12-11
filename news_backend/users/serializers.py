def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_bio": user.profile.bio
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