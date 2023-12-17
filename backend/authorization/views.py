from django.contrib.auth.models import User
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CrystalUser
from .serializers import AuthCodeSerializer, AuthPswSerializer, AuthByPhone
from .utils import create_oauth_links, OauthWay, get_user_info, create_payload_for_access_google_token, \
    create_payload_for_access_vk_token, get_vk_user_info, get_phone_code_from_api
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
        user_id, first_name, last_name = get_vk_user_info(token)

        text += f"user_id {user_id} , first_name {first_name} , last_name {last_name}"
    else:
        text += f"we have a problem with token response because {token_response.text}"
    return HttpResponse(text)


def googleOauthTest(request):
    text = "start "
    print('START')
    authorization_code = request.GET.get('code')
    print('[get code]', authorization_code)
    payload, token_url = create_payload_for_access_google_token(GOOGLE_OAUTH, authorization_code)
    print('[payload]', payload, token_url)
    token_response = requests.post(token_url, data=payload)
    print(token_response)
    if token_response.status_code == 200:
        access_token = token_response.json().get('id_token')
        email, name = get_user_info(access_token)
        text += f"succeed {email} {name}"
    else:
        text += f'fail with google response because {token_response.text}'
    return HttpResponse(text)


class CreateUserByPsw(APIView):
    serializer_class = AuthPswSerializer

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
                user = CrystalUser.objects.get(auth_type='psw', identifier=username)
                return Response({'result': 'This username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except CrystalUser.DoesNotExist:
                user = CrystalUser.objects.create_user(identifier=username, password=psw, auth_type='psw')
                return Response({'result': f'created {user}'}, status=status.HTTP_201_CREATED)


class ObtainTokenByPsw(APIView):
    serializer_class = AuthPswSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            psw = serializer.validated_data['password']
            try:
                user = CrystalUser.objects.get(auth_type='psw', identifier=username)
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
        text = "start "
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_vk_token(VK_OAUTH, authorization_code)
            token_response = requests.get(token_url, params=payload)
            if token_response.status_code == 200:
                token = token_response.json().get('access_token')
                user_id, first_name, last_name = get_vk_user_info(token)
                if not user_id:
                    return Response({'result': 'we have a problem with oauth steps . cant to get vk_user_id'},
                                    status=status.HTTP_409_CONFLICT)
                try:
                    user = CrystalUser.objects.get(auth_type='vk', identifier=user_id)
                except CrystalUser.DoesNotExist:
                    user = CrystalUser.objects.create_user(identifier=user_id,
                                                           auth_type='vk',
                                                           first_name=first_name,
                                                           last_name=last_name)
                token, created = Token.objects.get_or_create(user=user)
                return Response(data={"result": "success", "token": token}, status=status.HTTP_200_OK)
            else:
                text = f"we have a problem with token response because {token_response.text}"
                return Response(data={'result': text}, status=status.HTTP_409_CONFLICT)
        return Response(data={'result': 'Invalid Date'}, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenByPhone(ObtainTokenByVkCode):
    serializer_class = AuthByPhone

    def post(self, request):
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            if code:
                phone = serializer.validated_data.get('phone')
                user, created = CrystalUser.objects.get_or_create(identifier=phone, auth_type='phone')
                if created:
                    new_secure_code = get_phone_code_from_api(phone)
                    user.code = new_secure_code
                    user.save()
                    Response(data={'result': 'we need code again'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    saved_code = user.code
                    if str(code) == str(saved_code):
                        token, created = Token.objects.get_or_create(user=user)
                        Response(data={'token': token}, status=status.HTTP_200_OK)
                    else:
                        Response(data={'details': 'bad code'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                phone = serializer.validated_data.get('phone')
                secure_code = get_phone_code_from_api(phone)
                user, created = CrystalUser.objects.get_or_create(identifier=phone, auth_type='phone')
                user.code = secure_code
                user.save()
                return Response(data={'result': 'successfully sended code'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'result': f"Serializer is not valid {serializer.errors}"})


class ObtainTokenByEmail(ObtainTokenByVkCode):
    pass


class ObtainTokenByGoogleCode(APIView):
    serializer_class = AuthCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_google_token(GOOGLE_OAUTH, authorization_code)
            token_response = requests.post(token_url, data=payload)
            if token_response.status_code == 200:
                access_token = token_response.json().get('id_token')
                try:
                    email, name = get_user_info(access_token)
                except Exception as er:
                    return Response(data={'result': 'error', 'details': er})
                try:
                    user = User.objects.get(indefier=email, auth_type='google')
                except User.DoesNotExist:
                    user = CrystalUser.objects.create_user(identifier=email, auth_type='google')
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
        result = {'google_url': google_result,
                  'vk_url': vk_result}
        return Response(result)
