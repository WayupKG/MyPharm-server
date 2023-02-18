from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.user.models import UserActivateCode
from common.constans import DEFAULT_ERROR_MESSAGES
from common.validators import validate_user_email, validate_password, validate_activate_code
from workers import send_activated_code

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='email', read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'sur_name',
                  'gender', 'phone', 'address', 'is_pensioner',
                  'is_beneficiaries']


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'sur_name',
                  'gender', 'phone', 'address', 'is_pensioner',
                  'is_beneficiaries', 'password', 'password_confirm']

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        to_validate = validate_password(**data)
        if to_validate is False:
            raise ValidationError(
                DEFAULT_ERROR_MESSAGES.get('invalid_password_confirm'),
                'invalid_password_confirm'
            )
        return to_validate

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailSerializer(serializers.Serializer):
    """Сериализация email для отправки писем на почту"""
    email = serializers.EmailField()

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        if not validate_user_email(data.get('email')):
            raise ValidationError(
                DEFAULT_ERROR_MESSAGES.get('invalid_email'),
                "invalid_email"
            )
        return data

    def send_email(self):
        email = self.validated_data.get('email')
        send_activated_code.delay(email)


class PasswordResetSerializer(serializers.Serializer):
    """Сериализация для сброса пароля"""
    email = serializers.CharField(write_only=True)
    activate_code = serializers.IntegerField(write_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def validate(self, data: dict[str, str]) -> dict[str, str]:
        if not validate_user_email(data.get('email')):
            raise ValidationError(
                DEFAULT_ERROR_MESSAGES.get('invalid_email'),
                "invalid_email"
            )
        activate_codes = UserActivateCode.objects.filter(user__email=data.get('email'), code=data.get('activate_code'))
        if not activate_codes.exists():
            raise ValidationError(
                DEFAULT_ERROR_MESSAGES.get('no_activated_code'),
                'no_activated_code'
            )
        else:
            activate_code = activate_codes.first()
            if not validate_activate_code(activate_code.updated_at):
                raise ValidationError(
                    DEFAULT_ERROR_MESSAGES.get('invalid_activate_code'),
                    'invalid_activate_code'
                )
        to_validate = validate_password(**data)
        if to_validate is False:
            raise ValidationError(
                DEFAULT_ERROR_MESSAGES.get('invalid_password_confirm'),
                'invalid_password_confirm'
            )
        return to_validate