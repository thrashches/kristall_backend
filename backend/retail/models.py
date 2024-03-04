from django.db import models


class RetailOffice(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название офиса")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    working_hours = models.CharField(max_length=255, verbose_name="Рабочие часы")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='retail_offices/', verbose_name="Изображение")

    class Meta:
        verbose_name = "Офис продаж"
        verbose_name_plural = "Офисы продаж"
        ordering = ['id']

    def __str__(self):
        return f'{self.name}: {self.address}'
