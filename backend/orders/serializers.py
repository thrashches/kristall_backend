from django.db.models import F
from rest_framework import serializers

from goods.models import Product
from goods.serializers import SingleImageSerializer
from orders.models import Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'image',
        ]
        ref_name = "OrderProductSerializer"

    def get_image(self, obj: Product):
        if obj.images.exists():
            image = obj.images.first()
            return image.image_file.url
        return None


class OrderItemWriteOnlySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
        ]


class OrderItemReadOnlySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
        ]


class OrderReadOnlySerializer(serializers.ModelSerializer):
    items = OrderItemReadOnlySerializer(many=True, read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'items',
            'id',
            'number',
            'created_at',
            'price',
            'status',
        ]

    def get_price(self, order):
        items = order.items.all().annotate(
            price=F('product__price') * F('quantity')
        )
        return sum(item.price for item in items)


class OrderWriteOnlySerializer(serializers.ModelSerializer):
    items = OrderItemWriteOnlySerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'items',
        ]

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = super().create(validated_data)
        OrderItem.objects.bulk_create([OrderItem(order=order, **item) for item in items])
        return order

    def update(self, instance, validated_data, partial=False):
        items = validated_data.pop('items')
        order = super().update(instance, validated_data)
        OrderItem.objects.filter(order=order).delete()
        OrderItem.objects.bulk_create([OrderItem(order=order, **item) for item in items])
        return order

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return OrderReadOnlySerializer(instance, context=context).data


class CartItemWriteOnlySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'product',
        ]
