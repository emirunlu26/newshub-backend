"""Service file representing the service layer of the project.
It contains all service functions to handle requests related to users
Service functions implement the business logic.
"""
from django.contrib.auth import login
from .models import User

def register_user(register_data):
    """Service function that registers an user"""
    # Get request:
    request = register_data.get["request"]

    # Get required fields
    username = register_data.get("username")
    password = register_data.get("password")
    password_repeat = register_data.get("password_repeat")
    first_name = register_data.get("first_name")
    last_name = register_data.get("last_name")
    email = register_data.get("email")
    country = register_data.get("country")
    birth_date = register_data.get("birth_date")

    # Get optional fields
    gender = register_data.get("gender")

    # Check if the required fields are not empty
    if username is None:
        return {"message": {"content": "User Name field can not be empty.", "type": "error"}}, 400
    if password is None:
        return {"message": {"content": "Password field can not be empty.", "type": "error"}}, 400
    if password_repeat is None:
        return {"message": {"content": "Password must be repeated for validaton.", "type": "error"}}, 400
    if first_name is None:
        return {"message": {"content": "First Name field can not be empty.", "type": "error"}}, 400
    if last_name is None:
        return {"message": {"content": "Last Name field can not be empty.", "type": "error"}}, 400
    if email is None:
        return {"message": {"content": "Email field can not be empty.", "type": "error"}}, 400
    if country is None:
        return {"message": {"content": "Location field can not be empty.", "type": "error"}}, 400
    if birth_date is None:
        return {"message": {"content": "Birth date field can not be empty.", "type": "error"}}, 400

    # Check if username and email are unique:
    if User.objects.filter(username=username).exists():
        return {"message": {"content": "This user name is already used by an existing account.", "type": "error"}}, 400
    if User.objects.filter(email=email).exists():
        return {"message": {"content": "This email is already used by an existing account.", "type": "error"}}, 400

    # Check if username and password are valid
    if not User.is_username_valid(username):
        return {"message": {"content": "Invalid user name.", "type": "error"}}, 400
    if not User.is_password_valid(password):
        return {"message": {"content": "Invalid password.", "type": "error"}}, 400

    # Check if the repeated password matches with first password
    if password != password_repeat:
        return {"message": {"content": "Repeated password is different.", "type": "error"}}, 400

    # Create the user and set the required & optional fields
    new_user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    country=country,
                                    birth_date=birth_date,
                                    gender=gender)
    new_user.save()
    login(request=request, user=new_user)
    return {
        "message": {
            "content": "User created successfully",
            "type": "success"},
        "user_id": new_user.id,
        "redirect_url": ""
    }, 201

