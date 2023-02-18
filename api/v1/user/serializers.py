from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common.validators import validate_user_email, validate_password

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
                {"password_confirm": "Пароли не совпадают"}
            )
        return to_validate

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailSerializer(serializers.Serializer):
    """Сериализация email для отправки писем на почту"""
    email = serializers.EmailField()

    def validate(self, validated_data: dict[str, str]) -> dict[str, str]:
        if not validate_user_email(validated_data.get('email')):
            raise ValidationError(
                {"email": "Пользователь таким email'ом не найдено"}
            )
        return validated_data

    def send_email(self, *, protocol: str, domain: str):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)


class PasswordResetSerializer(serializers.Serializer):
    """Сериализация для сброса пароля"""
    activate_code = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def validate(self, validated_data: dict[str, str]) -> dict[str, str]:
        return validate_password(**validated_data)

    def update(self, instance, validated_data):
        if True:
            instance.set_password(validated_data.get('password'))
            instance.save()
            return instance
        raise ValidationError({"detail": "Код для сброса пароля недействительно."})