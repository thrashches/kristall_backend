f
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from backend.swagger_shema import schema_view


urlpatterns = [

    path('api/v1/', include('backend_api.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

