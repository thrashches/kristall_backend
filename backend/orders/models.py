from django.db import models
from django.db.models import F, Max

from authorization.models import CrystalUser
from goods.models import Product
from retail.models import RetailOffice


# Статусы заказов
IN_CART = 'in_cart'
PROCESSING = 'processing'
DONE = 'done'
DECLINE = 'decline'

# Префиксы номера заказа
CLIENT_WHOLESALE = 'W'
CLIENT_RETAIL = 'R'
DELIVERY_RETAIL = 'R'
DELIVERY_COURIER = 'C'


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (IN_CART, 'В корзине'),
        (PROCESSING, 'В обработке'),
        (DONE, 'Исполнен'),
        (DECLINE, 'Отменен'),
    ]

    number = models.CharField(null=True, blank=True, max_length=10, verbose_name="Номер заказа")
    user = models.ForeignKey(CrystalUser, related_name='orders', on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=IN_CART,
                              verbose_name="Статус заказа")
    delivery_time = models.DateTimeField(blank=True, null=True, verbose_name="Время доставки")
    comment = models.CharField(blank=True, max_length=4000, verbose_name="Комментарий")
    retail_office = models.ForeignKey(RetailOffice, on_delete=models.PROTECT, related_name='office', null=True,
                                      blank=True, verbose_name="Пункт выдачи")
    address = models.CharField(null=True, blank=True, max_length=200, verbose_name="Адрес")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ {self.id}"

    def save(self, *args, **kwargs):
        if not self.id:
            order_number = ''
            if self.user.is_wholesale:
                order_number += CLIENT_WHOLESALE
            else:
                order_number += CLIENT_RETAIL
            order_max_id = Order.objects.aggregate(max_id=Max('id')).get('max_id', 0)
            if not order_max_id:
                order_number += '-00000001'
            else:
                order_number += '-' + str(order_max_id + 1).zfill(8)
            self.number = order_number
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)

    class Meta:
        verbose_name = "Позиция в заказе"
        verbose_name_plural = "Позиции в заказах"

    def __str__(self):
        return f"Позиция {self.id} в заказе №{self.order.number}"
