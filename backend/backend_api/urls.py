from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from authorization.urls import auth_url_paterns
from authorization.views import ChangeUserDataViewSet
from backend_api.views import CategoryViewSet, ProductViewSet,  OrderViewSet

my_router = SimpleRouter()
my_router.register(r'menu', CategoryViewSet, basename='menu')
my_router.register(r'goods', ProductViewSet, basename='products')
my_router.register(r'mybasket',OrderViewSet, basename='basket')

my_router.register(r'users', ChangeUserDataViewSet, basename='chane_user_data')

urlpatterns = [
      # path('basket' , creataOrderView.as_view(), name='create'),
    ]

urlpatterns += my_router.urls
urlpatterns += auth_url_paterns
