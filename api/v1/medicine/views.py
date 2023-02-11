from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from apps.medicine.models import Category, Medicine
from api.v1.medicine import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'children', 'medicines']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['children']:
            self.serializer_class = serializers.CategoryChildrenSerializer
        if self.action in ['medicines']:
            self.serializer_class = serializers.MedicineListSerializer
        return self.serializer_class

    @action(methods=['GET'], detail=False)
    def children(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def medicines(self, *args, **kwargs):
        medicines = Medicine.objects.filter(category=self.get_object())
        serializer = self.get_serializer(medicines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.MedicineSerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'children']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['list']:
            self.serializer_class = serializers.MedicineListSerializer
        return self.serializer_class
