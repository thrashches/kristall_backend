from rest_framework import serializers
from goods.models import ProductImage, Product
from orders.models import Order, OrderItem




class ImageSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ['image_file']
        required = False


class ProductOrderSerializer(serializers.ModelSerializer):
    """такой сериализатор не работает."""
    id = serializers.IntegerField()
    name = serializers.CharField(source='title')
    price = serializers.IntegerField()
    image = ImageSerializer(source='images')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductOrderSerializer()
    quality = serializers.IntegerField

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
