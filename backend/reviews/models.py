from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок отзыва(общее впечатление)')
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(unique=True)
    published = models.BooleanField(default=False, verbose_name='Отображать на сайте')
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        verbose_name='Оценка')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-id']
