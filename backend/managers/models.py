from django.db import models
from .validators import phone_validator


class ManagerFeedback(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя клиента')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12,
                             validators=[
                                 phone_validator,
                             ],
                             blank=True, null=True, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время обращения')
    processed = models.BooleanField(default=False, verbose_name='Обработан')

    class Meta:
        verbose_name = 'Контакт клиента'
        verbose_name_plural = 'Контакты клиентов'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}: {self.created_at}'
