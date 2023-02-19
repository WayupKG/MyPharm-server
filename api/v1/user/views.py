from django.contrib.auth import get_user_model

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.v1.user import serializers

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsAdminUser]
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['me', 'update_me', 'destroy_me']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['create', 'password', 'password_reset']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['create']:
            return serializers.RegistrationSerializer
        if self.action in ['password']:
            return serializers.EmailSerializer
        if self.action in ['password_reset']:
            return serializers.PasswordResetSerializer
        return super().get_serializer_class()

    def get_object(self):
        if self.action in ['me', 'update_me', 'destroy_me']:
            return get_object_or_404(User, pk=self.request.user.id)
        return super().get_object()

    @action(["get"], detail=False)
    def me(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data, status.HTTP_200_OK)

    @me.mapping.patch
    def update_me(self, *args, **kwargs):
        return super().update(self.request, *args, **kwargs)

    @me.mapping.delete
    def destroy_me(self, *args, **kwargs):
        return super().destroy(self.request, *args, **kwargs)

    @action(['post'], detail=False)
    def password(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_email()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'detail': 'На вашу электронную почту отправлено разовый код.'
            },
            status=status.HTTP_200_OK,
            headers=headers
        )

    @action(['put'], detail=False)
    def password_reset(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'detail': 'Пароль успешно изменено.'
            },
            status=status.HTTP_200_OK,
            headers=headers
        )
