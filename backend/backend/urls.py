from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from authorization.views import ChangePasswordView
from backend.swagger_shema import schema_view
from backend_api.urls import router_goods

urlpatterns = [
    path('crystal/admin/', admin.site.urls),
    path('crystal/api/v1/', include(router_goods.urls)),
    path('crystal/api/v1/auth/', include('authorization.urls')),
    path('crystal/api/v1/', ChangePasswordView.as_view(), name='change_password'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('crystal/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('crystal/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
