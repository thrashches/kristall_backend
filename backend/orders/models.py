from django.db import models
from authorization.models import CrystalUser
from goods.models import Product


# TODO:: круто
# TODO: Модели согласно задаче https://github.com/users/thrashches/projects/7?pane=issue&itemId=43006322
# OPTIMIZE:  А вот это почему не подсвечиваеся???


class Order(models.Model):
    STATUS_CHOICES = (
        ('in_basket', 'В корзине'),
        ('in_work', 'В обработке'),
        ('done', 'Исполнен'),
        ('decline', 'Отменен'),
    )
    number = models.IntegerField(null=True)
    user = models.ForeignKey(CrystalUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='in_basket')
    summary_items = models.IntegerField(null=True)
    summary_calories = models.IntegerField(null=True)
    comment = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"OrderItem: {self.id} | {self.user.username} | {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
