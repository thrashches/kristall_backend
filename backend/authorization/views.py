from django.contrib.auth.models import User
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CrystalUser
from .serializers import AuthCodeSerializer, AuthPswSerializer
from .utils import create_oauth_links, OauthWay, get_user_info, create_payload_for_access_google_token, \
    create_payload_for_access_vk_token
from backend.settings import GOOGLE_OAUTH, VK_OAUTH
from rest_framework.authtoken.models import Token
from django.http import HttpResponse


def vkOauthTest(request):
    text = "start "
    authorization_code = request.GET.get('code')
    payload, token_url = create_payload_for_access_vk_token(VK_OAUTH, authorization_code)
    token_response = requests.get(token_url, params=payload)
    if token_response.status_code == 200:
        text += "we have a token \n "
        token = token_response.json().get('access_token')
        text += str(token)
    else:
        text += f"we have a problem with token response because {token_response.text}"
    return HttpResponse(text)


def gooleOauthTest(request):
    text = "start"
    authorization_code = request.GET.get('code')
    payload, token_url = create_payload_for_access_google_token(GOOGLE_OAUTH, authorization_code)
    token_response = requests.post(token_url, data=payload)
    if token_response.status_code == 200:
        access_token = token_response.json().get('id_token')
        try:
            email, name = get_user_info(access_token)
            text += f"succeed {email} {name}"
        except Exception as er:
            text += str(er)
    else:
        text += f'fail with google response because {token_response.text}'
    return HttpResponse(text)


class CreateUserByPsw(APIView):
    serializer_class = AuthPswSerializer
    """ЧЕ СВАГЕР ДОКУМЕНТАЦИЮ ВОТ ТАК НАДО ПИСАТЬ? ПОЧЕМУ НЕ РАБОТАЕТ АВТОГЕНЕРАЦИЯ? Хотя федор конечно , догадыватся.
    """

    @swagger_auto_schema(
        request_body=AuthPswSerializer,
        responses={
            201: "Successfully created",
            400: "This username already exists"
        },
        operation_summary="Create User by Password",
        operation_description="Create a new user by providing a unique username and password."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            psw = serializer.validated_data['password']
            try:
                user = CrystalUser.objects.get(username=username)
                return Response({'result': 'This username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except CrystalUser.DoesNotExist:
                user = CrystalUser.objects.create_user(username=username, password=psw, auth_type='psw')
                return Response({'result': f'created {user}'}, status=status.HTTP_201_CREATED)


class ObtainTokenByPsw(APIView):
    serializer_class = AuthPswSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            psw = serializer.validated_data['password']

            try:
                user = CrystalUser.objects.get(username=username)
                if user.check_password(psw):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'result': 'success', 'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'result': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            except CrystalUser.DoesNotExist:
                return Response({'result': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenByVkCode(APIView):
    serializer_class = AuthCodeSerializer

    def post(self, request):
        text = "start dich"
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_vk_token(VK_OAUTH, authorization_code)
            token_response = requests.get(token_url, params=payload)
            if token_response.status_code == 200:
                text += "we have a token \n "
                token = token_response.json().get('access_token')
                text += str(token)
            else:
                text += f"we have a problem with token response because {token_response.text}"

        return Response(data={'result': 'not ready yet'})


class ObtainTokenByPhone(ObtainTokenByVkCode):
    pass


class ObtainTokenByEmail(ObtainTokenByVkCode):
    serializer_class = AuthCodeSerializer
    pass


class ObtainTokenByGoogleCode(APIView):
    serializer_class = AuthCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_google_token(GOOGLE_OAUTH, authorization_code)
            print('INFO code->payload->token_url', authorization_code, payload, token_url, sep="\n")
            token_response = requests.post(token_url, data=payload)
            if token_response.status_code == 200:
                access_token = token_response.json().get('id_token')
                try:
                    email, name = get_user_info(access_token)
                except Exception as er:
                    return Response(data={'result': 'error', 'details': er})
                try:
                    user = User.objects.filter(email=email, auth_type='google')
                except User.DoesNotExist:
                    user = CrystalUser.objects.create_user(email=email, username=name, auth_type='google')
                token, created = Token.objects.get_or_create(user=user)
                return Response(data={"result": "success", "token": token}, status=status.HTTP_200_OK)
            else:
                return Response(data={'result': 'fail',
                                      'details': f'cant to obtain google access token because {token_response.text}'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            errors = serializer.errors
            return Response(data={"result": "error", "details": f" serializer{errors}"},
                            status=status.HTTP_400_BAD_REQUEST)


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
