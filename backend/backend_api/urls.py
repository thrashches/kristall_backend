from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'menu', CategoryViewSet, basename='menu')
router.register(r'goods', ProductViewSet, basename='products')
router.register(r'goods/(?P<product_id>\d+)/images', ProductImageViewSet, basename='product-images')

