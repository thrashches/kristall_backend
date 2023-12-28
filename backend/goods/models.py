import os
from uuid import uuid4
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория меню')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес')
    energy = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Энергетическая ценность')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    visible = models.BooleanField(default=True, verbose_name='Отображать на сайте')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


def image_upload_path(instance, filename):
    # FIXME: Убрать из моделей
    ext = filename.split('.')[-1]
    unique_filename = f'{uuid4()}.{ext}'
    return os.path.join('product_images', unique_filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image_file = models.ImageField(upload_to=image_upload_path, verbose_name='Изображение')
    visible = models.BooleanField(default=True, verbose_name='Отображать на сайте')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self):
        return f"Картинка для {self.product.title}"
