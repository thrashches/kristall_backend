
from django.contrib import admin
from django.urls import path, re_path, include
from backend.swagger_shema import schema_view
from backend_api.urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router_goods.urls)),
    path('api/v1/auth/', include('authorization.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
