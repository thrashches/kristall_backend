from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order, IN_CART, OrderItem
from orders.permissions import IsOrderOwner
from orders.serializers import OrderReadOnlySerializer, OrderWriteOnlySerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrderReadOnlySerializer
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

    # @swagger_auto_schema(
    #     method='delete',
    #     responses={204: openapi.Response('Успешно', OrderShemaSerializer()), 400: openapi.Response('Ошибка запроса')},
    #     operation_summary="Очистить корзину",
    #     operation_description="Удаляет все элементы  OrderItems из Orders со статусом CART."
    # )
    # @swagger_auto_schema(
    #     method='put',
    #     request_body=OrderReadOnlySerializer(),
    #     responses={200: openapi.Response('Успешное', OrderShemaSerializer()),
    #                400: openapi.Response('Ошибка запроса')},
    #     operation_summary="Добавить в корзину товар",
    #     operation_description="Добавить к Order присланные OrderItems."
    # )
    # @swagger_auto_schema(
    #     method='patch',
    #     request_body=OrderReadOnlySerializer(),
    #     responses={200: openapi.Response('Успех', OrderShemaSerializer()),
    #                400: openapi.Response('Ошибка запроса')},
    #     operation_summary="Удалить товар из корзины",
    #     operation_description="Ищет по product id OrdeItem который относится к последниму Order и удаляет его"
    # )
    # @swagger_auto_schema(
    #     method='get',
    #     responses={200: openapi.Response('Успешно'), 400: openapi.Response('Ошибка запроса')},
    #     operation_summary="Создать заказ из корзины",
    #     operation_description="Изменяет статус последнего Order со статусом CART на WORK"
    # )
    @action(detail=False, methods=['PUT', 'PATCH', 'DELETE', 'GET'])
    def cart(self, request):
        queryset = Order.objects.filter(user=self.request.user, status__in=[IN_CART])
        order = queryset.latest('created_at')
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        elif request.method in ['DELETE']:
            items = OrderItem.objects.filter(order=order)
            items.delete()
            return Response(status=203)
