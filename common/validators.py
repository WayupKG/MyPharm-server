from typing import Any
from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_activate_code(created_date):
    pass_reset_date = timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)
    diff_between_current_and_created = timezone.now() - created_date
    if pass_reset_date > diff_between_current_and_created:
        return True
    return False


def validate_password(**validate_data: dict[str, Any]) -> dict[str, Any]:
    if validate_data.get('password') != validate_data.pop('password_confirm'):
        return False
    return validate_data


def validate_user_email(email: str) -> bool:
    user = User.objects.filter(email=email).exists()
    return True if user else False
