from django.urls import path
from authorization.views import ObtainTokenByGoogleCode, CreateAuthLinks, ObtainTokenByPsw, ObtainTokenByVkCode, \
    ObtainTokenByPhone, ObtainTokenByEmail, CreateUserByPsw, googleOauthTest, vkOauthTest

urlpatterns = [
    path('get_token/psw/', ObtainTokenByPsw.as_view(), name='get token by psw and username'),
    path('get_token/oauth2/google/', ObtainTokenByGoogleCode.as_view(), name='get token by Oauth Google'),
    path('get_token/oauth2/vk/', ObtainTokenByVkCode.as_view(),name='get token by Oauth VK'),
    path('get_token/email/', ObtainTokenByEmail.as_view(),name='get token by email code'),
    path('get_token/phone/', ObtainTokenByPhone.as_view(), name='get token by Phone number'),
    path('get_oauth_links/', CreateAuthLinks.as_view(), name='create_oauth_links'),
    path('create_user/psw/', CreateUserByPsw.as_view(), name='create_user_with psw and username'),
    path('get_token/oauth/google/', googleOauthTest, name='testing page googleOatuth'),
    path('get_token/oauth/vk/', vkOauthTest, name='testing page vkOauth'),
]
