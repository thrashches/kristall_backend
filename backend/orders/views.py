from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order, DONE, WORK, DECLINE, CART
from orders.permissions import IsOrderOwner
from orders.serializers import OrderSerializer


class AwesomeMarvelousFantasticViewSet(viewsets.GenericViewSet,
                                       mixins.CreateModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.ListModelMixin):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status__in=[WORK, DONE])

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permission() for permission in [IsAuthenticated]]
        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):
        return {'view': self}

    @action(detail=False, methods=['PUT', 'PATCH', 'DELETE'])
    def cart(self, request):
        queryset = Order.objects.filter(user=self.request.user, status__in=[CART])
        order = queryset.latest('created_at')
        serializer = self.get_serializer(order, data=request.data)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=200)
