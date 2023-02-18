from typing import Any

from django.contrib.auth import get_user_model

User = get_user_model()


def validate_password(**validate_data: dict[str, Any]) -> dict[str, Any]:
    if validate_data.get('password') != validate_data.pop('password_confirm'):
        return False
    return validate_data


def validate_user_email(email: str) -> bool:
    user = User.objects.filter(email=email).exists()
    return True if user else False
