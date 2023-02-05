from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from common.upload_to_file import company_logo_img, company_contract_file


class Company(models.Model):
    """Фармацевтические компании"""
    title = models.CharField('Название', max_length=225)
    description = models.TextField('Описание', null=True, blank=True)
    logo = ProcessedImageField(verbose_name='Логотип', upload_to=company_logo_img,
                               format='webp', options={'quality': 90})

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Фармацевтический компания'
        verbose_name_plural = 'Фармацевтические компании'

    def __str__(self):
        return self.title


class ContractCompany(models.Model):
    """Контракт с компанией"""
    company = models.OneToOneField(Company, verbose_name='Компания', on_delete=models.CASCADE, related_name='contract')
    description = models.TextField('Описание', null=True, blank=True)
    file = models.FileField('Файл контракта', upload_to=company_contract_file)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    end_date = models.DateField('Окончание договора')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Контракт с компанией'
        verbose_name_plural = 'Контракты с компаниями'

    def __str__(self):
        return f"{self.company} - {self.is_active}"


class Pharmacy(models.Model):
    """Аптека"""
    title = models.CharField('Название', max_length=225)
    description = models.TextField('Описание', null=True, blank=True)
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.CASCADE, related_name='pharmacies')
    region = models.CharField(max_length=32)  # Надо доработать
    address = models.CharField(max_length=32)  # Надо доработать
    cell_phone = models.CharField(max_length=32)  # Надо доработать

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Аптека'
        verbose_name_plural = 'Аптеки'

    def __str__(self):
        return f"{self.company} - {self.title}"