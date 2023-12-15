from django.http import HttpResponse
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CrystalUser
from .serializers import AuthCodeSerializer
from .utils import create_oauth_links, OauthWay, get_user_info, create_payload_for_access_google_token
from backend.settings import GOOGLE_OAUTH


class OAuthCookieGoogleInjection(View):
    serializer_class = AuthCodeSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.GET)
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_google_token(GOOGLE_OAUTH, authorization_code)
            token_response = requests.post(token_url, data=payload)
            if token_response.status_code == 200:
                access_token = token_response.json().get('id_token')
                try:
                    email, name = get_user_info(access_token)
                    result = (email, name)

                except Exception as er:

                    return HttpResponse(f'Fail in getting user info from google {er}')
                try:
                    user = CrystalUser.objects.get(email=email)
                    print('old user', user)
                except CrystalUser.DoesNotExist:
                    print('new user')
                    user = CrystalUser.objects.create_user(email=email, username=name, auth_type='google')
                user_id = user.id
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = HttpResponse(f"SUCCESS, I want to redirect from here {result}. Check cookie. We have access "
                                        f"token here now")

                response.set_cookie(key='access_token', value=access_token, max_age=3600, secure=True,
                                    httponly=True)
                response.set_cookie(key='refresh_token', value=refresh_token, max_age=3600, secure=True,
                                    httponly=True)
                return response


            else:
                return HttpResponse(f"We dont have a google access token. Why? 400 token response")
        return HttpResponse(f"Error: method is not allowed")


class TokenObtainOauth(TokenObtainPairView):
    pass


class TokenObtainPhone(TokenObtainPairView):
    pass


class TokenObtainMail(TokenObtainPairView):
    pass


class CreateAuthLinks(APIView):
    def get(self, request):
        google_link, comment = create_oauth_links(OauthWay.GOOGLE)
        if google_link:
            google_result = google_link
        else:
            google_result = comment
        vk_link, comment = create_oauth_links(OauthWay.VK)
        if vk_link:
            vk_result = vk_link
        else:
            vk_result = comment
        result = {'google_link': google_result,
                  'vk_ling': vk_result}
        return Response(result)
