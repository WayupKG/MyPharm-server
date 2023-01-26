from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from apps.user.managers import UserManager
from common.constans import GENDER_MEN, GENDER_WOMEN
from common.upload_to_file import avatar_img


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь"""
    GENDER = (
        (GENDER_MEN, 'Мужской'),
        (GENDER_WOMEN, 'Женский'),
    )
    email = models.EmailField('email', unique=True)
    last_name = models.CharField('Фамилия', max_length=40)
    first_name = models.CharField('Имя', max_length=40)
    sur_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    gender = models.CharField('Пол', max_length=10, choices=GENDER)
    phone = models.CharField('Телефон', max_length=120)
    avatar = models.ImageField('Изображение', upload_to=avatar_img, blank=True, null=True)
    address = models.CharField('Адрес', max_length=128, blank=True, null=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_pensioner = models.BooleanField(default=False)
    is_beneficiaries = models.BooleanField(default=False)

    activate_code = models.PositiveIntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'sur_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Возвращает full_name."""
        if self.sur_name:
            return f"{self.first_name} {self.last_name} {self.sur_name}".strip()
        return f"{self.first_name} {self.last_name}".strip()
