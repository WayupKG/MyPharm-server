from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserActivateCode

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'phone']


@admin.register(UserActivateCode)
class UserActivateCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'counter', 'updated_at']