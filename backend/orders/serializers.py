from django.db import models
from rest_framework import serializers
from goods.models import Product
from orders.models import OrderItem, Order, Book


class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)


class OrderItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    images = serializers.ListField(child=serializers.CharField(), read_only=True)
    def create(self, validated_data):
        product_id = validated_data['product']
        quantity = validated_data['quantity']
        order = validated_data['order']

        order_item = OrderItem.objects.create(
            product_id=product_id,
            quantity=quantity,
            order=order,
        )
        return order_item

    def to_representation(self, instance):
        id = instance['product']
        product = Product.objects.get(id=id)

        data = {
            'id': product.id,
            'quantity': instance['quantity'],
            'name': product.title,
            'price': product.price,
            'images': [image.image_file.url for image in product.images.all()]
        }
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(write_only=True, many=True)
    items_ = serializers.SerializerMethodField(read_only=True)



    def get_items_(self,instance):

