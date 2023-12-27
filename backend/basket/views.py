from django.db.models import Prefetch
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basket.models import Order, OrderItem
from basket.serializers import orderIncomeSerializer, orderItemSerializer, orderSerializer
from goods.models import Product


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

    def create(self, request):
        item_serializers, items_queryset, summary = [], [], 0
        itemss_data=[]
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
                # FIXME: А вдруг картинок будет много на один продукт может возвращать не строку а список всё таки?
                image = images_url_list[0]
            else:
                image = None

            item_data = {'order': order.id,
                         'product': product.id,
                         'quantity': quantity,
                         'image': image
                         }

            # item_serializers.append(orderItemSerializer(data=item_data))
            itemss_data.append(item_data)
            items_queryset.append(OrderItem(order=order,
                                            product=product,
                                            quantity=quantity))
            summary += quantity*product.price
        print(order,type(order))

        order_data = {
            'id': order.id,
            'number': order.number,
            'date': order.created_at,
            'price': summary,
            'status': order.status,
            'items': itemss_data
        }
        print("we are here",order_data)
        answer = orderSerializer(data=order_data)
        answer.is_valid()
        return Response(answer.data, status=200)

    def put(self, request):
        return Response("PUT request processed")

    def patch(self, request):

        return Response("PATCH request processed")
