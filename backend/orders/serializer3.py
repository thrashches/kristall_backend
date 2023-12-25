from rest_framework import serializers
from goods.serializers import ProductSerializer
from orders.models import Order, OrderItem



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    quality = serializers.IntegerField

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
