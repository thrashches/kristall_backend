from rest_framework.routers import SimpleRouter

from backend_api.views import CategoryViewSet, ProductViewSet

router_goods = SimpleRouter()
router_goods.register(r'menu', CategoryViewSet, basename='menu')
router_goods.register(r'goods', ProductViewSet, basename='products')
