from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basket.serializers import orderIncomeSerializer, orderSerializer


class BasketViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer(self):
        serializer = orderIncomeSerializer(data=self.request.data)
        return serializer

    def create(self, request):
        income = self.get_serializer()
        if not income.is_valid():
            return Response(income.errors, status=400)
        # user = self.get_object()
        # order = Order.objects.create(user=user)
        print(income.data)
        return Response(status=200)

    def put(self, request):
        # Логика для метода PUT
        # args и kwargs могут содержать параметры маршрута, если они указаны в URL
        return Response("PUT request processed")

    def patch(self, request):
        # Логика для метода PATCH
        # args и kwargs могут содержать параметры маршрута, если они указаны в URL
        return Response("PATCH request processed")
