from django.urls import path
from authorization.views import ObtainTokenByGoogleCode, CreateAuthLinks, ObtainTokenByPsw, ObtainTokenByVkCode, \
    ObtainTokenByPhone, googleOauthTest, vkOauthTest

urlpatterns = [
    path('email/', ObtainTokenByPsw.as_view(), name='get token by psw and email'),
    path('google/', ObtainTokenByGoogleCode.as_view(), name='get token by Oauth Google'),
    path('vk/', ObtainTokenByVkCode.as_view(),name='get token by Oauth VK'),
    path('phone/', ObtainTokenByPhone.as_view(), name='get token by Phone number'),


    path('links/', CreateAuthLinks.as_view(), name='create_oauth_links'),


    path('get_token/oauth/google/', googleOauthTest, name='testing page googleOatuth'),
    path('get_token/oauth/vk/', vkOauthTest, name='testing page vkOauth'),
]
