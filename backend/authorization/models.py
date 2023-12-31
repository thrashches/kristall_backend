import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

PHONE = 'phone'
MAIL = 'mail'
GOOGLE = 'google'
VK = 'vk'
PASSWORD = 'password'


class CrystalUser(AbstractUser):
    AUTH_TYPE_CHOICES = [
        (PHONE, 'По телефону'),
        (MAIL, 'По почте'),
        (GOOGLE, 'Google'),
        (VK, 'VK'),
        (PASSWORD, 'По паролю'),
    ]

    auth_type = models.CharField(
        max_length=10,
        choices=AUTH_TYPE_CHOICES,
        null=False,
        blank=False,
        default=PASSWORD,
        verbose_name='Тип авторизации',
    )
    identifier = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Идентификатор',
    )

    code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Код',
    )

    def save(self, *args, **kwargs):
        user_uuid = self.generate_uuid()
        if not self.username:
            self.username = user_uuid
        if not self.identifier:
            self.identifier = user_uuid
        super().save(*args, **kwargs)

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['auth_type', 'identifier'],
                name='unique_auth_type_identifier',
            )
        ]

    def __str__(self):
        return self.username
