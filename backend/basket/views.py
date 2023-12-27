from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basket.models import Order, OrderItem
from basket.serializers import orderIncomeSerializer, orderSerializer
from goods.models import Product


class MyPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BasketViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer(self):
        serializer = orderIncomeSerializer(data=self.request.data)
        return serializer

    def get_queryset(self, pk_items: list):
        product_with_images = Product.objects.prefetch_related('images').filter(pk__in=pk_items)
        return product_with_images

    @action(detail=False, methods=['put', 'get', 'post'])
    def basket(self, request):

        item_serializers, items_queryset, summary = [], [], 0
        items_data = []
        paginator = MyPagination()

        if request.method == 'POST':
            income = self.get_serializer()
            if not income.is_valid():
                return Response(income.errors, status=400)

            income_items = income.data.get('items_dict')
            products = self.get_queryset(income.data.get("products_pk"))
            user = self.get_object()
            order = Order.objects.create(user=user)

            for product in products:
                images = product.images.all()
                quantity = income_items[product.id]
                if images:
                    images_url_list = [image.image_file.url for image in images]
                    image = images_url_list[0]
                else:
                    image = None

                item_data = {'order': order.id,
                             'product': product.id,
                             'quantity': quantity,
                             'image': image
                             }
                items_data.append(item_data)
                items_queryset.append(OrderItem(order=order,
                                                product=product,
                                                quantity=quantity))
                summary += quantity * product.price

            OrderItem.objects.bulk_create(items_queryset)

            order_data = {
                'id': order.id,
                'number': order.number,
                'date': order.created_at,
                'price': summary,
                'status': order.status,
                'items': items_data
            }

        elif request.method == 'PUT':
            income = self.get_serializer()
            if not income.is_valid():
                return Response(income.errors, status=400)

            income_items = income.data.get('items_dict')
            products = self.get_queryset(income.data.get("products_pk"))
            user = self.get_object()
            order = Order.objects.filter(status='in_basket', user=user).latest('created_at')
            if not order:
                return Response(status=400)

            order_items = OrderItem.objects.filter(order=order)
            order_items.delete()

            for product in products:
                images = product.images.all()
                quantity = income_items[product.id]
                if images:
                    images_url_list = [image.image_file.url for image in images]
                    image = images_url_list[0]
                else:
                    image = None

                item_data = {'order': order.id,
                             'product': product.id,
                             'quantity': quantity,
                             'image': image
                             }
                items_data.append(item_data)
                items_queryset.append(OrderItem(order=order,
                                                product=product,
                                                quantity=quantity))
                summary += quantity * product.price

            OrderItem.objects.bulk_create(items_queryset)

            order_data = {
                'id': order.id,
                'number': order.number,
                'date': order.created_at,
                'price': summary,
                'status': order.status,
                'items': items_data
            }

        elif request.method == 'GET':
            user = self.get_object()
            order = Order.objects.filter(status='in_basket', user=user).latest('created_at')

            items_set = OrderItem.objects.filter(order=order)
            quantity_dict = {item.product.id: item.quantity for item in items_set}
            products_pk = quantity_dict.keys()
            products = self.get_queryset(products_pk)

            for product in products:
                images = product.images.all()
                quantity = quantity_dict[product.id]
                if images:
                    images_url_list = [image.image_file.url for image in images]
                    # FIXME: А вдруг картинок будет много на один продукт может возвращать не строку а список всё таки? #image = images_url_list
                    image = images_url_list[0]
                else:
                    image = None

                item_data = {'order': order.id,
                             'product': product.id,
                             'quantity': quantity,
                             'image': image
                             }
                items_data.append(item_data)
                items_queryset.append(OrderItem(order=order,
                                                product=product,
                                                quantity=quantity))
                summary += quantity * product.price

            OrderItem.objects.bulk_create(items_queryset)

            order_data = {
                'id': order.id,
                'number': order.number,
                'date': order.created_at,
                'price': summary,
                'status': order.status,
                'items': items_data
            }

        answer = orderSerializer(data=order_data)
        answer.is_valid()
        paginated_response = paginator.get_paginated_response(answer.data)
        return Response(paginated_response, status=200)
