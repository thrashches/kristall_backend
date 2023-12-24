
from django.urls import path

from authorization.views import ObtainTokenByGoogleCode, CreateAuthLinks, ObtainTokenByPsw, ObtainTokenByVkCode, \
    ObtainTokenByPhone, creating_google_oauth_test, creating_vk_oauth_test

auth_url_paterns = [
    path('auth/email/', ObtainTokenByPsw.as_view(), name='get_token_by_psw_and_email'),
    path('auth/google/', ObtainTokenByGoogleCode.as_view(), name='get_token_by_oauth_google'),
    path('auth/vk/', ObtainTokenByVkCode.as_view(), name='get_token_by_oauth_vk'),
    path('auth/phone/', ObtainTokenByPhone.as_view(), name='get_token_by_phone_number'),

    path('auth/links/', CreateAuthLinks.as_view(), name='create_oauth_links'),
    path('tests/get_token/oauth/google/', creating_google_oauth_test, name='testing_page_google_oauth'),
    path('tests/get_token/oauth/vk/', creating_vk_oauth_test, name='testing_page_vk_oauth'),
]