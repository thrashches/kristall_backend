from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet

router_goods = DefaultRouter()
router_goods.register(r'menu', CategoryViewSet, basename='menu')
router_goods.register(r'goods', ProductViewSet, basename='products')
router_goods.register(r'goods/(?P<product_id>\d+)/images/', ProductImageViewSet, basename='product-images')

