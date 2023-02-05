from rest_framework.serializers import ModelSerializer

from apps.company.models import Company, ContractCompany, Pharmacy


class CompanySerializer(ModelSerializer):
    """Сериализация Компании"""
    class Meta:
        model = Company
        fields = ['id', 'title', 'description', 'logo', 'created_at', 'updated_at']


class CompanyListSerializer(ModelSerializer):
    """Сериализация списка компании"""
    class Meta:
        model = Company
        fields = ['id', 'title', 'logo']


class PharmacySerializer(ModelSerializer):
    """Сериализация аптек"""
    company = CompanyListSerializer(many=False)

    class Meta:
        model = Pharmacy
        fields = ['id', 'title', 'description', 'company', 'region', 'address',
                  'cell_phone', 'is_active', 'created_at', 'updated_at']


class PharmacyListSerializer(ModelSerializer):
    """Сериализация списка аптек"""
    class Meta:
        model = Pharmacy
        fields = ['id', 'title', 'region', 'address', 'cell_phone']