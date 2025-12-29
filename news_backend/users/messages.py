from news_backend import settings

# ERROR MESSAGES
def print_empty_field_error(field_name):
    return {
        "content": field_name + " field can not be empty.",
        "type": "error",
    }


BIRTH_DATE_INVALID = {
    "content": f"Invalid birth date. Accepted format is: {settings.DATE_INPUT_FORMATS[0]}",
    "type": "error"
}

GENDER_INVALID = {
    "content": "Invalid gender.",
    "type": "error"
}

EMAIL_ALREADY_TAKEN = {
    "content": "This email is already used by an existing account.",
    "type": "error"
}

FONT_COLOUR_INVALID = {
    "content": "Invalid font colour.",
    "type": "error",
}

FONT_SIZE_INVALID = {
    "content": "Invalid font size.",
    "type": "error"
}

FONT_TYPE_INVALID = {
    "content": "Invalid font type.",
    "type": "error",
}

PASSWORD_CONFIRM_UNMATCHED = {
    "content": "Repeated password is different.",
    "type": "error"
}

PASSWORD_INVALID = {
    "content": "Invalid password.",
    "type": "error"
}

THEME_INVALID = {
    "content": "Invalid theme.",
    "type": "error"
}

USERNAME_ALREADY_TAKEN = {
    "content": "This user name is already used by an existing account.",
    "type": "error"
}

USERNAME_INVALID = {
    "content": "Invalid user name.",
    "type": "error"
}

USER_NOT_FOUND = {
    "content": "User with the given id is not found.",
    "type": "error"
}

# WARNING MESSAGES
USER_ALREADY_FOLLOWED = {
    "content": "You're already following this user.",
    "type": "warning"
}

USER_ALREADY_SUBSCRIBED = {
    "content": "Your account has already been upgraded to premium.",
    "type": "warning",
}

USER_NOT_FOLLOWED_YET = {
    "content": "You're not following this user already.",
    "type": "warning"
}

USER_NOT_SUBSCRIBED_YET = {
    "content": "Your account has already been not premium.",
    "type": "warning"
}

# SUCCESS MESSAGES
def print_user_found_message(user_type):
    return {
        "content": user_type + " " + "user with the given id retrieved successfully",
        "type": "success"
    }


BOOKMARKED_ARTICLES_RETRIEVED_SUCCESS = {
    "content": "The list of bookmarked articles is retrieved successfully.",
    "type": "success",
}

FOLLOWED_CATEGORIES_RETRIEVED_SUCCESS = {
    "content": "The list of followed categories is retrieved successfully.",
    "type": "success"
}

FOLLOWED_TAGS_RETRIEVED_SUCCESS = {
    "content": "The list of followed tags is retrieved successfully.",
    "type": "success"
}

FOLLOWED_USERS_RETRIEVED_SUCCESS = {
    "content": "The list of followed users is retrieved successfully.",
    "type": "success"
}

FOLLOWERS_RETRIEVED_SUCCESS = {
    "content": "The list of followers is retrieved successfully.",
    "type": "success"
}

PROFILE_PICTURE_RETRIEVED_SUCCESS = {
    "content": "Profile picture is retrieved successfully.",
    "type": "success"
}

UI_CUSTOMIZATION_SETTINGS_RETRIEVED_SUCCESS = {
    "content": "UI customization settings are retrieved successfully.",
    "type": "success"
}

UI_CUSTOMIZATION_SETTINGS_UPDATED_SUCCESS = {
    "content": "UI customization settings are updated successfully.",
    "type": "success"
}

USER_CREATED_SUCCESS = {
    "content": "User created successfully",
    "type": "success"
}

USER_FOLLOWED_SUCCESS = {
    "content": "User is followed successfully.",
    "type": "success"
}

USER_PROFILE_RETRIEVED_SUCCESS = {
    "content": "User profile is retrieved successfully.",
    "type": "success"
}

USER_PROFILE_SETTINGS_RETRIEVED_SUCCESS = {
    "content": "Profile settings are retrieved successfully.",
    "type": "success"
}

USER_PROFILE_UPDATED_SUCCESS = {
    "content": "Profile settings are updated successfully.",
    "type": "success"
}

USER_SUBSCRIBED_SUCCESS = {
    "content": "Your account is upgraded to premium successfully.",
    "type": "success"
}

USER_UNFOLLOWED_SUCCESS = {
    "content": "User is unfollowed successfully.",
    "type": "success"
}

USER_UNSUBSCRIBED_SUCCESS = {
    "content": "Your subscription has been terminated successfully.",
    "type": "success"
}
