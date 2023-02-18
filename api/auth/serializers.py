from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD
    token_class = None

    default_error_messages = {
        'invalid_email': _("Пользователь с такой электронной почтой не существует."),
        'invalid_password': _(
            'Пожалуйста, введите правильный пароль. Обратите внимание, что пароль чувствителен к регистру.'),
        'inactive': _("Ваша учетная запись находится на рассмотрении."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()

    def validate_email(self, value):
        email = User.objects.filter(email__iexact=value.lower())
        if email.exists():
            if email[0].is_active:
                return value.lower()
            raise exceptions.AuthenticationFailed(
                self.default_error_messages.get('inactive'),
                'inactive'
            )
        raise exceptions.AuthenticationFailed(
            self.default_error_messages.get('invalid_email'),
            'invalid_email'
        )

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["invalid_password"],
                "invalid_password",
            )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
