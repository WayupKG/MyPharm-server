from django.contrib import admin

from .models import Company, ContractCompany, Pharmacy


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']


@admin.register(ContractCompany)
class ContractCompanyAdmin(admin.ModelAdmin):
    list_display = ['company', 'is_active', 'end_date', 'created_at', 'updated_at']


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'region', 'address', 'cell_phone', 'is_active', 'created_at', 'updated_at']
