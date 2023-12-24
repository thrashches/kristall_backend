from django.urls import path
from rest_framework.routers import SimpleRouter

from authorization.urls import auth_url_paterns
from authorization.views import ChangeUserDataViewSet
from backend_api.views import CategoryViewSet, ProductViewSet

router_goods = SimpleRouter()
router_goods.register(r'menu', CategoryViewSet, basename='menu')
router_goods.register(r'goods', ProductViewSet, basename='products')

urlpatterns = [
    path('users/', ChangeUserDataViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='user-detail'),
    path('users/me/', ChangeUserDataViewSet.as_view({'put': 'me'}), name='user-change-password'),
]
urlpatterns += router_goods.urls
urlpatterns += auth_url_paterns
