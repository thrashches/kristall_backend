from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from authorization.views import UserViewSet, ObtainTokenByPsw, ObtainTokenByGoogleCode, ObtainTokenByVkCode, \
    ObtainTokenByPhone, CreateAuthLinks, creating_google_oauth_test, creating_vk_oauth_test, YandexAuthTokenAPIView
from backend.swagger_shema import schema_view
from backend_api.views import CategoryViewSet, ProductViewSet
from managers.views import ManagerFeedbackViewSet
from orders.views import OrderViewSet
from retail.views import RetailOfficeViewSet
from reviews.views import ReviewViewSet

router = SimpleRouter()
router.register('menu', CategoryViewSet, basename='menu')
router.register('goods', ProductViewSet, basename='products')
router.register('users', UserViewSet, basename='user')
router.register('orders', OrderViewSet, basename='orders')
router.register('retail', RetailOfficeViewSet, basename='retail')
router.register('reviews', ReviewViewSet, basename='reviews')
router.register('managers', ManagerFeedbackViewSet, basename='managers')

urlpatterns = [
    path('auth/email/', ObtainTokenByPsw.as_view(), name='get_token_by_psw_and_email'),
    path('auth/google/', ObtainTokenByGoogleCode.as_view(), name='get_token_by_oauth_google'),
    path('auth/vk/', ObtainTokenByVkCode.as_view(), name='get_token_by_oauth_vk'),
    path('auth/phone/', ObtainTokenByPhone.as_view(), name='get_token_by_phone_number'),
    path('auth/yandex/token/', YandexAuthTokenAPIView.as_view(), name='yandex_auth_token'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/links/', CreateAuthLinks.as_view(), name='create_oauth_links'),
    path('tests/get_token/oauth/google/', creating_google_oauth_test, name='testing_page_google_oauth'),
    path('tests/get_token/oauth/vk/', creating_vk_oauth_test, name='testing_page_vk_oauth'),

]
urlpatterns += router.urls
