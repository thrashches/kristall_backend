from django.urls import path
from authorization.views import ObtainTokenByGoogleCode, CreateAuthLinks, ObtainTokenByPsw, ObtainTokenByVkCode, \
    ObtainTokenByPhone, googleOauthTest, vkOauthTest


urlpatterns = [
    path('email/', ObtainTokenByPsw.as_view(), name='get_token_by_psw_and_email'),
    path('google/', ObtainTokenByGoogleCode.as_view(), name='get_token_by_oauth_google'),
    path('vk/', ObtainTokenByVkCode.as_view(), name='get_token_by_oauth_vk'),
    path('phone/', ObtainTokenByPhone.as_view(), name='get_token_by_phone_number'),

    path('links/', CreateAuthLinks.as_view(), name='create_oauth_links'),

    path('get_token/oauth/google/', googleOauthTest, name='testing_page_google_oauth'),
    path('get_token/oauth/vk/', vkOauthTest, name='testing_page_vk_oauth'),
]
