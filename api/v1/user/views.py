from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH

from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['me', 'update_me', 'destroy_me']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        if self.action in ['me', 'update_me', 'destroy_me']:
            return get_object_or_404(User, pk=self.request.user.id)
        return super().get_object()

    @action(["get"], detail=False)
    def me(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @me.mapping.patch
    def update_me(self, *args, **kwargs):
        return super().update(self.request, *args, **kwargs)

    @me.mapping.delete
    def destroy_me(self, *args, **kwargs):
        return super().destroy(self.request, *args, **kwargs)
