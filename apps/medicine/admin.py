from django.contrib import admin

from .models import Category, Medicine, Stock, PharmacyMedicine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'sub_category', 'created_at', 'updated_at']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_prescription_required', 'is_active', 'created_at', 'updated_at']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percent', 'created_at', 'updated_at']


@admin.register(PharmacyMedicine)
class PharmacyMedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'pharmacy', 'stock', 'price', 'total_price', 'created_at', 'updated_at']