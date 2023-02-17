from django.core.validators import MaxValueValidator
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from common.upload_to_file import medicine_img


class Category(models.Model):
    """Категория препаратов"""
    parent = models.ForeignKey('self', verbose_name='Под категория', on_delete=models.SET_NULL,
                               related_name='children', null=True, blank=True)
    title = models.CharField('Название', max_length=255)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Medicine(models.Model):
    """Препарат"""
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT)
    image = ProcessedImageField(verbose_name='Изображение', upload_to=medicine_img,
                                format='webp', options={'quality': 90})
    is_prescription_required = models.BooleanField(verbose_name='Рецептурный препарат', default=False)
    is_active = models.BooleanField(verbose_name='Является активным', default=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Препарат'
        verbose_name_plural = 'Препараты'

    def __str__(self):
        return self.title


class Stock(models.Model):
    """Акция для препаратов"""
    title = models.CharField('Название', max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return f"{self.title} - {self.discount_percent}%"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__discount_percent = self.discount_percent
    #
    # def save(self, *args, **kwargs):
    #     if self.discount_percent != self.__discount_percent:
    #         for subscription in self.subscriptions.all():
    #             set_price.delay(subscription.id)
    #     return super().save(*args, **kwargs)


class PharmacyMedicine(models.Model):
    """Аптечные Препараты"""
    pharmacy = models.ForeignKey('company.Pharmacy', verbose_name='Аптека',
                                 on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey(Medicine, verbose_name='Препарат',
                                 on_delete=models.CASCADE, related_name='pharmacies')
    stock = models.ForeignKey(Stock, verbose_name='Акция', on_delete=models.SET_NULL,
                              related_name='medicines', null=True, blank=True)

    price = models.DecimalField('Цена', max_digits=5, decimal_places=2)
    total_price = models.DecimalField('Цена после скидки', max_digits=5, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Аптечный Препарат'
        verbose_name_plural = 'Аптечные Препараты'

    def __str__(self):
        return f"{self.pharmacy} - {self.medicine}"
