from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from goods.models import Category, Product
from goods.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(visible=True)
    serializer_class = ProductSerializer

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
