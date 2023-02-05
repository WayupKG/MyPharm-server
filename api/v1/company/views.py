from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from apps.company.models import Company, ContractCompany, Pharmacy
from api.v1.company import serializers


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['list']:
            self.serializer_class = serializers.CompanyListSerializer
        elif self.action in ['pharmacies']:
            self.serializer_class = serializers.PharmacyListSerializer
        return self.serializer_class

    @action(methods=['GET'], detail=True)
    def pharmacies(self, *args, **kwargs):
        pharmacies = Pharmacy.objects.filter(company=self.get_object())
        serializer = self.get_serializer(pharmacies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PharmacyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.PharmacySerializer
    queryset = Pharmacy.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ['list']:
            self.serializer_class = serializers.PharmacyListSerializer
        return self.serializer_class
