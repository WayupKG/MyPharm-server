from django import forms
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, TreeRelatedFieldListFilter
from mptt.forms import TreeNodeChoiceField

from .models import Category, Medicine, Stock, PharmacyMedicine


# admin.site.register(Category, MPTTModelAdmin)

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'title',
                    'related_medicines_cumulative_count',
                    'created_at', 'updated_at')
    list_display_links = ('title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add cumulative product count
        qs = Category.objects.add_related_count(qs, Medicine,
                'category', 'medicine_cumulative_count', cumulative=True)
        return qs

    def related_medicines_cumulative_count(self, instance):
        return instance.medicine_cumulative_count
    related_medicines_cumulative_count.short_description = 'Related medicines (in tree)'


class TreeCategoryForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Category.objects.all(), level_indicator='+---')


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    form = TreeCategoryForm
    list_display = ['title', 'category', 'is_prescription_required', 'is_active', 'created_at', 'updated_at']
    field1 = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="(Nothing)")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percent', 'created_at', 'updated_at']


@admin.register(PharmacyMedicine)
class PharmacyMedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'pharmacy', 'stock', 'price', 'total_price', 'created_at', 'updated_at']