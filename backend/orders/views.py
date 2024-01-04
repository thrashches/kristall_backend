from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order, IN_CART, OrderItem
from orders.permissions import IsOrderOwner
from orders.serializers import OrderReadOnlySerializer, OrderWriteOnlySerializer, CartItemWriteOnlySerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    # serializer_class = OrderReadOnlySerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return OrderReadOnlySerializer
        elif self.action == 'create':
            return OrderWriteOnlySerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(status=IN_CART).filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Создание нового заказа",
        responses={201: openapi.Response('Успешно', OrderReadOnlySerializer),
                   400: openapi.Response('Ошибка в запросе')},
    )
    def create(self, request, *args, **kwargs):
        """Создание нового заказа"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(method='GET', responses={200: openapi.Response('Успешно', OrderReadOnlySerializer)})
    @swagger_auto_schema(method='PUT', request_body=OrderWriteOnlySerializer,
                         responses={200: openapi.Response('Успешно', OrderReadOnlySerializer)})
    @swagger_auto_schema(method='PATCH', request_body=CartItemWriteOnlySerializer,
                         responses={200: openapi.Response('Успешно', OrderReadOnlySerializer)})
    @action(detail=False, methods=['PUT', 'PATCH', 'DELETE', 'GET'])
    def cart(self, request):
        """Просмотр корзины, добавление товаров в корзину и удаление товаров из корзины"""
        cart, created = Order.objects.get_or_create(user=request.user, status=IN_CART)
        if request.method == "GET":
            return Response(OrderReadOnlySerializer(cart).data)
        elif request.method == "PUT":
            """Добавление товаров в корзину"""
            serializer = OrderWriteOnlySerializer(cart, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == "PATCH":
            """Добавление товара в корзину"""
            serializer = CartItemWriteOnlySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = serializer.validated_data.get('product')
            if OrderItem.objects.filter(order=cart, product=product).exists():
                order_item = OrderItem.objects.get(order=cart, product=product)
                order_item.quantity += 1
                order_item.save()
            else:
                OrderItem.objects.create(order=cart, product=product)
            return Response(OrderReadOnlySerializer(cart).data)
        elif request.method == "DELETE":
            """Очистка всей корзины"""
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
