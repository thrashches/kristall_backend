from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import OrderItemSerializer

class MySecretOrderView(APIView):
    serializer_class = OrderItemSerializer

    @swagger_auto_schema(
        request_body=OrderItemSerializer
        ,
        responses={
            200: openapi.Response('Success', schema=OrderItemSerializer),
            400: openapi.Response('Bad Request', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Details of the error'),
                }
            )),
        },
    )
    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            return Response(ser.data, status=200)
        else:
            return Response(ser.errors, status=400)


# class OrderViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.ListModelMixin,
#                    viewsets.GenericViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
