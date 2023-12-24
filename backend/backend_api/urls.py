from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from authorization.urls import auth_url_paterns
from authorization.views import ChangeUserDataViewSet
from backend_api.views import CategoryViewSet, ProductViewSet

my_router = SimpleRouter()
my_router.register(r'menu', CategoryViewSet, basename='menu')
my_router.register(r'goods', ProductViewSet, basename='products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', ChangeUserDataViewSet.as_view({
        'get': 'retrieve',
        # 'put': 'update',
        # 'delete': 'destroy'
        }),
         name='user_detail'),
    # path('users/me/', ChangeUserDataViewSet.as_view({'put': 'me'}), name='user-change-password'),
]
urlpatterns += my_router.urls
urlpatterns += auth_url_paterns
