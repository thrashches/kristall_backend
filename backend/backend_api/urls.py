rom django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'menu', CategoryViewSet, basename='menu')
router.register(r'goods', ProductViewSet, basename='goods')
router.register(r'goods/(?P<product_id>\d+)/images', ProductImageViewSet, basename='product-images')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]