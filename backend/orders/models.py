from django.db import models

from authorization.models import CrystalUser
from goods.models import Product

CART = 'in_basket'
WORK = 'in_work'
DONE = 'done'
DECLINE = 'decline'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (CART, 'В корзине'),
        (WORK, 'В обработке'),
        (DONE, 'Исполнен'),
        (DECLINE, 'Отменен'),
    ]

    number = models.CharField(null=True, blank=True, max_length=10, verbose_name="Номер заказа")
    user = models.ForeignKey(CrystalUser, related_name='items', on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=CART, verbose_name="Статус заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} user {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)

    class Meta:
        verbose_name = "Позиция в заказе"
        verbose_name_plural = "Позиции в заказах"

    def __str__(self):
        return f"OrderItem {self.id} for Order {self.order.number}"
