from django.contrib.auth.models import AbstractUser
from django.db import models


class CrystalUser(AbstractUser):
    AUTH_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('mail', 'Mail'),
        ('google', 'Google'),
        ('vk', 'VK'),
    ]
    auth_type = models.CharField(
        max_length=10,
        choices=AUTH_TYPE_CHOICES,
        null=False
    )

    class Meta:
        verbose_name = 'Crystal User'
        verbose_name_plural = 'Crystal Users'


