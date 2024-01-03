from django.db import models

from authorization.models import CrystalUser
from goods.models import Product

IN_CART = 'in_cart'
PROCESSING = 'processing'
DONE = 'done'
DECLINE = 'decline'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (IN_CART, 'В корзине'),
        (PROCESSING, 'В обработке'),
        (DONE, 'Исполнен'),
        (DECLINE, 'Отменен'),
    ]

    number = models.CharField(null=True, blank=True, max_length=10, verbose_name="Номер заказа")
    user = models.ForeignKey(CrystalUser, related_name='items', on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=IN_CART, verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)

    class Meta:
        verbose_name = "Позиция в заказе"
        verbose_name_plural = "Позиции в заказах"

    def __str__(self):
        return f"Позиция {self.id} в заказе №{self.order.number}"
