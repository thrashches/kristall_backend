import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

PHONE = 'phone'
MAIL = 'mail'
YANDEX = 'yandex'
VK = 'vk'
PASSWORD = 'password'


class CrystalUser(AbstractUser):
    AUTH_TYPE_CHOICES = [
        (PHONE, 'По телефону'),
        (MAIL, 'По почте'),
        (YANDEX, 'Yandex'),
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
    yandex_id = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Yandex ID'
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
    is_wholesale = models.BooleanField(null=False,
                                       default=False,
                                       verbose_name='Оптовик')
    email = models.EmailField(_("email address"), blank=True, null=True, default=None)
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения',
    )
    company = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Компания',
    )
    bonus_balance = models.IntegerField(default=0, verbose_name="Бонусные баллы")

    def save(self, *args, **kwargs):
        if not self.username:
            user_uuid = self.generate_uuid()
            self.username = user_uuid
        return super(CrystalUser, self).save(*args, **kwargs)

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['auth_type', 'email', 'phone', 'username', 'yandex_id'],
                name='unique_auth_type_identifier',
            ),
        ]

    def __str__(self):
        if self.auth_type in [MAIL, YANDEX, VK]:
            return self.email
        elif self.auth_type == PHONE:
            return self.phone
        elif self.auth_type == PASSWORD:
            return self.username
        return self.username
