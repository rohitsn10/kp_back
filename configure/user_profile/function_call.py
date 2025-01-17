from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from user_profile.models import *
from rest_framework.request import Request

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


def process_file_ids(file_ids):
    if isinstance(file_ids, str):
        file_ids = [id.strip() for id in file_ids.split(',') if id.strip()]
    return [int(id) for id in file_ids if id.isdigit()]


def get_file_data(request: Request, obj, field_name: str):
    field = getattr(obj, field_name, None)

    if field:
        if isinstance(field, models.Manager):
            return [
                {
                    "id": str(item.id),
                    "url": request.build_absolute_uri(getattr(item, field_name).url),
                    "created_at": item.created_at.isoformat(),
                    "updated_at": item.updated_at.isoformat(),
                }
                for item in field.all()
            ]
        elif hasattr(field, 'url'):
            return {
                "id": str(field.id),
                "url": request.build_absolute_uri(field.url),
                "created_at": field.created_at.isoformat(),
                "updated_at": field.updated_at.isoformat()
            }

    return None


def get_expense_project_attachments_file_data(request: Request, obj, field_name: str):
    field = getattr(obj, field_name, None)

    if field:
        if isinstance(field, models.Manager):  
            return [
                {
                    "id": str(item.id),
                    "url": request.build_absolute_uri(item.expense_project_attachments.url),
                    "created_at": item.created_at.isoformat(),
                }
                for item in field.all()
            ]
        elif hasattr(field, 'url'):
            return {
                "id": str(field.id),
                "url": request.build_absolute_uri(field.url),
                "created_at": field.created_at.isoformat(),
            }

    return None


def get_client_details_file_data(request: Request, obj, field_name: str):
    field = getattr(obj, field_name, None)

    if field:
        # Handle ManyToManyField relationships
        if isinstance(field, models.Manager):
            return [
                {
                    "id": str(item.id),
                    "url": request.build_absolute_uri(getattr(item, field_name).url) if hasattr(getattr(item, field_name), 'url') else None,
                    "created_at": item.created_at.isoformat(),
                    "updated_at": item.updated_at.isoformat(),
                }
                for item in field.all()
            ]
        
        # Handle single FileField relationships (e.g., AdharCard, PanCard, etc.)
        elif hasattr(field, 'url'):
            return {
                "id": str(field.id),
                "url": request.build_absolute_uri(field.url) if hasattr(field, 'url') else None,
                "created_at": field.created_at.isoformat(),
                "updated_at": field.updated_at.isoformat()
            }

    return None

