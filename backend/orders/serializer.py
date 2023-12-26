from rest_framework import serializers
from goods.models import Product, ProductImage
from orders.models import Order, OrderItem

"""Решение без ModelSerializer
Как такое делать через ModelSerializer и ModelViewSet  в три строчки это надо обладать более высоким уровнем мастерства.
Либо мне нужно больше времени. 

Чёт я убился об эти вьюсеты  помагите. 
 """


class OrderItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    product_ = serializers.SerializerMethodField()

    def get_product_(self, obj):
        try:
            prod = self.validated_data['product']
            prod_id = prod.id
            prod_name = prod.title
            prod_price = prod.price
            image = ProductImage.objects.get(product=prod_id)
            prod_image = image.image_file
        except Product.DoesNotExist:
            prod_id = 0
            prod_name = "does not exists"
            prod_price = 0
            prod_image = "does not exists"
        except ProductImage.DoesNotExist:
            prod_image = "does not exists"
        except Exception as er:
            raise serializers.ValidationError(f'We hava problem in serializer Item: {er}')
        data = {
            "id": prod_id,
            "name": prod_name,
            "price": prod_price,
            "image": prod_image
        }
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = data.pop('product_')
        return data


class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)


    def create(self, validated_data):
        items = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user)
        items_data, summary = self.__create_items_data(items, order)
        order_data = self.__create_order_data(order, items_data, summary)
        validated_data = {**validated_data, **order_data}
        return validated_data

    def custom_update(self):
        validated_data = self.validated_data
        income_items = validated_data.pop('items')
        user = self.context['request'].user
        latest_order = Order.objects.filter(user=user, status='in_basket').order_by('-created_at').first()
        items, summary = self.__create_items_data(items=income_items, order=latest_order)
        order_data = self.__create_order_data(latest_order, items, summary)
        validated_data = {**validated_data, **order_data}
        return validated_data

    def to_representation(self, instance):
        income_data = super().to_representation(instance)
        income_items = income_data.pop('items')
        user = self.context.get('request').user
        latest_order = Order.objects.filter(user=user, status='in_basket').order_by('-created_at').first()
        items, summary = self.__create_items_data(items=income_items, order=latest_order)
        data = self.__create_order_data(latest_order, items, summary)
        return data

    @staticmethod
    def __create_order_data(order, items_data, summary):
        data = {'id': order.id, 'number': order.number, 'date': order.created_at, 'status': order.status,
                'items': items_data, 'price': summary}
        return data

    @staticmethod
    def __create_items_data(items, order):
        # Вот это ЛЮТЫЕ костыли. А там были цветочки! )))
        # Я это переделаю чтоб запрос один к бд был. Как такое делается в три строчки яхз

        items_data = []
        summary = 0
        for item in items:
            product = item.get('product')
            quantity = item.get('quantity')
            OrderItem.objects.create(order=order, **item)
            try:
                image = ProductImage.objects.get(product=product)
                image_path = image.image_file
            except ProductImage.DoesNotExist:
                image_path = None

            #ВИдимо это всё должно через сериализаторы быть.
            item_data = {"product": {"id": product.id, "name": product.title, "price": product.price,
                                     "image": image_path},
                         "quantity": quantity
                         }
            items_data.append(item_data)
            summary += product.price * quantity
        return items_data, summary
