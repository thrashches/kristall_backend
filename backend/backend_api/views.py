from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from goods.models import Category, Product
from goods.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from orders.models import Order, OrderItem
from orders.serializer import OrderItemSerializer, OrderSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    @action(detail=True, methods=['get'])
    def images(self, request, pk):
        product = self.get_object()
        images = product.images.all()
        serializer = ProductImageSerializer(images, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class OrderViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=OrderSerializer, responses={status.HTTP_201_CREATED: OrderSerializer})
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        request_body=OrderSerializer, responses={status.HTTP_201_CREATED: OrderSerializer})
    @action(detail=False, methods=['put'])
    def update_order(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.custom_update()
            return Response(data)
        return Response(serializer.errors, status=400)

    @action(detail=False,methods=['patch'])
    def change_order(self,request):
        pass




