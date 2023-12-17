import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class CrystalUser(AbstractUser):
    AUTH_TYPE_CHOICES = [
        ('phone', 'Phone'),
        ('mail', 'Mail'),
        ('google', 'Google'),
        ('vk', 'VK'),
        ('psw', 'PSW'),
    ]

    auth_type = models.CharField(
        max_length=10,
        choices=AUTH_TYPE_CHOICES,
        null=False
    )
    identifier = models.CharField(
        max_length=100,
        null=False,
    )

    code = models.CharField(
        max_length=20,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.generate_username()
        super().save(*args, **kwargs)

    def generate_username(self):
        return str(uuid.uuid4())

    class Meta:
        verbose_name = 'Crystal User'
        verbose_name_plural = 'Crystal Users'
        unique_together = ('identifier', 'auth_type')
