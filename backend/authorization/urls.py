from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authorization.views import TokenObtainOauth, TokenObtainPhone, TokenObtainMail, CreateAuthLinks, \
    OAuthCookieGoogleInjection

urlpatterns = [
    path('get_token/psw/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('get_token/oauth/google/', OAuthCookieGoogleInjection.as_view(), name='token_obtain_from_oauth'),
    path('get_token/oauth/vk/', TokenObtainOauth.as_view(), name='token_obtain_from_oauth'),
    path('get_token/phone/', TokenObtainPhone.as_view(), name='token_obtain_from_phone'),
    path('get_token/mail/', TokenObtainMail.as_view(), name='token_obtain_from_mail'),
    path('get_token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_oauth_links', CreateAuthLinks.as_view(),name='create_oauth_links')
]
