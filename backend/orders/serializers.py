from django.db.models import Prefetch
from rest_framework import serializers
from goods.models import Product, ProductImage
from orders.models import Order, OrderItem, WORK

"""
instance = super().update(instance, validated_data) вот это главная функция у меня должна быть.

видимо, надо больше времени .

хотяя может так меньше запросов в бд...

"""


class OrderItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)


class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)

    def _items_dict(self, validated_data):
        items = validated_data['items']
        return {item['product']: item['quantity'] for item in items}

    def to_representation(self, instance: Order):

        representation = super().to_representation(instance)

        items = (OrderItem.objects.filter(order=instance).prefetch_related(
            Prefetch(
                'product__images',
                queryset=ProductImage.objects.filter(visible=True),
                to_attr='visible_images'
            )
        ).select_related('product'))
        items_data = []
        summary = 0
        for item in items:
            product = item.product
            image_url = product.visible_images[0].image_file.url if product.visible_images else None
            item_data = {
                'product': {
                    'id': product.id,
                    'name': product.title,
                    'price': product.price,
                    'image': image_url
                },
                'quantity': item.quantity
            }
            summary = item.quantity * product.price
            items_data.append(item_data)

        representation['items'] = items_data
        representation['id'] = instance.pk
        representation['number'] = instance.number
        representation['price'] = summary
        representation['status'] = instance.status

        if self.context.get('view').action == 'list':
            representation.pop('status')

        return representation

    def create(self, validated_data):

        queryset = []
        items_dict = self._items_dict(validated_data)
        user = self.context.get('view').request.user

        order = Order.objects.create(user=user)
        pk_ = items_dict.keys()
        product_with_images = Product.objects.prefetch_related('images').filter(pk__in=pk_)

        for product in product_with_images:
            quantity = items_dict[product.id]
            queryset.append(OrderItem(order=order,
                                      product=product,
                                      quantity=quantity))
        OrderItem.objects.bulk_create(queryset)
        return order

    def update(self, instance, validated_data):

        queryset = []
        order = instance
        items_dict = self._items_dict(validated_data)
        pk_ = items_dict.keys()
        product_with_images = Product.objects.prefetch_related('images').filter(pk__in=pk_)

        if self.context['view'].request.method == 'PUT':
            for product in product_with_images:
                quantity = items_dict[product.id]
                queryset.append(OrderItem(order=order,
                                          product=product,
                                          quantity=quantity))
            OrderItem.objects.bulk_create(queryset)
    # FIXME: Я не понял механизм отправления в работу из корзины. Написале его тут но чет мне подксказывает ты имелл ввиду что то иное
            order.status = WORK
            order.save()
            return order

        elif self.context['view'].request.method == 'PATCH':
            items = OrderItem.objects.filter(product__id__in=pk_)
            items.delete()
            order.status = WORK
            return order

        elif self.context['view'].request.method == 'DELETE':
            items = OrderItem.objects.filter(order=order)
            items.delete()
            return order
