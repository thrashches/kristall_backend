from django.db import models
from authorization.models import CrystalUser
from goods.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('in_basket', 'В корзине'),
        ('in_work', 'В обработке'),
        ('executed', 'Исполнен'),
        ('decline', 'Отменен'),
    ]

    user = models.ForeignKey(CrystalUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_basket')

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Item {self.id} - Order {self.order.id}"
