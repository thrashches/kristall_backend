from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order, IN_CART, OrderItem
from orders.permissions import IsOrderOwner
from orders.serializers import OrderWriteOnlySerializer, CartItemWriteOnlySerializer, \
    OrderReadOnlyWholesalerSerializer, OrderReadOnlySingleSerializer, OrderWriteOnlyCreateSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    permission_classes = [IsOrderOwner]
    queryset = Order.objects.all()
    pagination_class = None

    def check_for_wholesaler(self):
        """Это костыль? """
        if self.request.user.is_wholesale:
            return OrderReadOnlyWholesalerSerializer
        else:
            return OrderReadOnlySingleSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return self.check_for_wholesaler()
        elif self.action == 'create':
            return OrderWriteOnlyCreateSerializer
        return self.check_for_wholesaler()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(status=IN_CART).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=OrderWriteOnlyCreateSerializer,
        operation_description="Создание нового заказа",
        responses={201: openapi.Response('Успешно', OrderReadOnlySingleSerializer),
                   400: openapi.Response('Ошибка в запросе')},
    )
    def create(self, request, *args, **kwargs):
        """Создание нового заказа"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(method='GET', responses={200: openapi.Response('Успешно', OrderReadOnlySingleSerializer)},
                         operation_description='Если использует оптовый покупатель поля retail_office и address'
                                               'не будут отображены')
    @swagger_auto_schema(method='PUT', request_body=OrderWriteOnlySerializer,
                         responses={200: openapi.Response('Успешно', OrderReadOnlySingleSerializer)},
                         operation_description='Если использует оптовый покупатель поля retail_office и address'
                                               'не будут отображены')
    @swagger_auto_schema(method='PATCH', request_body=CartItemWriteOnlySerializer,
                         responses={200: openapi.Response('Успешно', OrderReadOnlySingleSerializer)},
                         operation_description='Если использует оптовый покупатель поля retail_office и address'
                                               'не будут отображены')
    @action(detail=False, methods=['PUT', 'PATCH', 'DELETE', 'GET'])
    def cart(self, request):
        """Просмотр корзины, добавление товаров в корзину и удаление товаров из корзины"""
        cart = Order.objects.filter(user=request.user, status=IN_CART).order_by('created_at').last()
        if not cart:
            cart = Order.objects.create(user=request.user, status=IN_CART)
        if request.method == "GET":
            serializer = self.get_serializer_class()
            return Response(serializer(cart).data)
        elif request.method == "PUT":
            """Добавление товаров в корзину (с перезаписью всех товаров)"""
            serializer = OrderWriteOnlySerializer(cart, data=request.data,context={'request':self.request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == "PATCH":
            """Добавление товара в корзину (добавить товары в уже существующую корзину)"""
            serializer = CartItemWriteOnlySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = serializer.validated_data.get('product')
            if OrderItem.objects.filter(order=cart, product=product).exists():
                order_item = OrderItem.objects.get(order=cart, product=product)
                order_item.quantity += 1
                order_item.save()
            else:
                OrderItem.objects.create(order=cart, product=product)
            return_serializer = self.get_serializer_class()
            return Response(return_serializer(cart).data)
        elif request.method == "DELETE":
            """Очистка всей корзины"""
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
