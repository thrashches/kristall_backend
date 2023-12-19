from django.db import models
from authorization.models import CrystalUser
from backend_api.models import Product


class Order(models.Model):
    user = models.ForeignKey(CrystalUser, on_delete=models.CASCADE)
    calories = models.IntegerField()
    price = models.IntegerField()
    is_paid = models.BooleanField()


class Basket(models.Model):
    order = models.ForeignKey(CrystalUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
