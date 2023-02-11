from rest_framework import serializers

from apps.medicine.models import Category, Medicine


class FilterCategoryListSerializer(serializers.ListSerializer):
    """Фильтр категории, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveCategorySerializer(serializers.Serializer):
    """Вывод рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoryChildrenSerializer(serializers.ModelSerializer):
    """Сериализация Категории (Children)"""
    children = RecursiveCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        list_serializer_class = FilterCategoryListSerializer
        fields = ['id', 'title', 'children']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация Категории (parent=None)"""

    class Meta:
        model = Category
        list_serializer_class = FilterCategoryListSerializer
        fields = ['id', 'parent', 'title']
        extra_kwargs = {'parent': {'write_only': True}}


class MedicineSerializer(serializers.ModelSerializer):
    """Сериализация препаратов"""

    class Meta:
        model = Medicine
        fields = ['id', 'title', 'description', 'category', 'image',
                  'is_prescription_required', 'created_at', 'updated_at']


class MedicineListSerializer(serializers.ModelSerializer):
    """Сериализация списка препаратов"""

    class Meta:
        model = Medicine
        fields = ['id', 'title', 'category', 'image', 'is_prescription_required']
