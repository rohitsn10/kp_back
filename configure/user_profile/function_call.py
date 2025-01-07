from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from user_profile.models import *

def authenticate_user_by_email(email, password):
    """
    Authenticate a user based on their email and password.

    Args:
        email (str): The email of the user.
        password (str): The password provided by the user.

    Returns:
        user (CustomUser): Authenticated user instance or None if authentication fails.
    """
    User = get_user_model()
    try:
        # Retrieve the user by email
        user = CustomUser.objects.get(email=email)
        if user and check_password(password, user.password):
            return user
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
    return None
