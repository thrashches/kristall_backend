from django.db import models
from authorization.models import CrystalUser
from goods.models import Product


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('in_basket', 'В корзине'),
        ('in_work', 'В обработке'),
        ('done', 'Исполнен'),
        ('desline', 'Отменен'),
    ]
    number = models.CharField(null=True, blank=False, max_length=10)
    user = models.ForeignKey(CrystalUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='in_basket')

    def __str__(self):
        return f"Order {self.id} user {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"OrderItem {self.id} for Order {self.order.number}"


