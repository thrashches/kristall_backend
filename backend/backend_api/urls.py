from django.urls import path
from rest_framework.routers import SimpleRouter

from authorization.views import ChangeUserDataViewSet
from backend_api.views import CategoryViewSet, ProductViewSet

router_goods = SimpleRouter()
router_goods.register(r'menu', CategoryViewSet, basename='menu')
router_goods.register(r'goods', ProductViewSet, basename='products')


urlpatterns = [
    path('', ChangeUserDataViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='user-detail'),
    path('me/', ChangeUserDataViewSet.as_view({'put': 'me'}), name='user-change-password'),
]
