import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from backend_api.serializers import ErrorSerializer, SuccessSerializer
from .models import CrystalUser, MAIL, YANDEX
from .serializers import AuthCodeSerializer, AuthPasswordSerializer, AuthByPhoneSerializer, OAuthUrlsSerializer, \
    UserSerializer, PasswordSerializer, RegistrationSerializer, YandexAuthSerializer
from .utils import create_oauth_links, OauthWay, get_user_info, create_payload_for_access_google_token, \
    create_payload_for_access_vk_token, get_vk_user_info, get_phone_code_from_api


User = get_user_model()


def creating_vk_oauth_test(request):
    text = "start "
    authorization_code = request.GET.get('code')
    vk_secret = settings.VK_OAUTH
    payload, token_url = create_payload_for_access_vk_token(vk_secret, authorization_code)
    token_response = requests.get(token_url, params=payload)
    if token_response.status_code == 200:
        text += "we have a token \n "
        token = token_response.json().get('access_token')
        text += str(token)
        user_id, first_name, last_name = get_vk_user_info(token)
        text += f"user_id {user_id} , first_name {first_name} , last_name {last_name}"
    else:
        text += f"Проблемы с токеном: {token_response.text}"
    return HttpResponse(text)


def creating_google_oauth_test(request):
    google_credientals = settings.GOOGLE_OAUTH
    text = "start "
    print('START')
    authorization_code = request.GET.get('code')
    print('[get code]', authorization_code)
    payload, token_url = create_payload_for_access_google_token(google_credientals, authorization_code)
    print('[payload]', payload, token_url)
    token_response = requests.post(token_url, data=payload)
    print(token_response)
    if token_response.status_code == 200:
        access_token = token_response.json().get('id_token')
        email, name = get_user_info(access_token)
        text += f"succeed {email} {name}"
    else:
        text += f'Проблема при ответе сервиса google {token_response.text}'
    return HttpResponse(text)


class CreateUserByPsw(APIView):
    # FIXME: Это все зарефакторить, тут кровь из глаз
    serializer_class = AuthPasswordSerializer

    @swagger_auto_schema(
        request_body=AuthPasswordSerializer,
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
            password = serializer.validated_data['password']
            try:
                user = CrystalUser.objects.get(auth_type=MAIL, identifier=username)
                return Response({'result': 'Такой пользователь уже существует!'}, status=status.HTTP_400_BAD_REQUEST)
            except CrystalUser.DoesNotExist:
                user = CrystalUser.objects.create_user(identifier=username, password=password, auth_type='password')
                return Response({'result': f'Пользователь создан!'}, status=status.HTTP_201_CREATED)


class ObtainTokenByPsw(APIView):
    serializer_class = AuthPasswordSerializer

    @swagger_auto_schema(
        request_body=AuthPasswordSerializer,
        responses={
            200: openapi.Response('Token', schema=openapi.Schema(type='object', properties={
                'token': openapi.Schema(type='string', description='Generated token'),
            })),
            400: openapi.Response('Error', schema=openapi.Schema(type='object', properties={
                'error': openapi.Schema(type='string', description='Invalid password or validation error'),
            })),
            404: openapi.Response('Error', schema=openapi.Schema(type='object', properties={
                'error': openapi.Schema(type='string', description='User does not exist'),
            })),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = CrystalUser.objects.get(auth_type=MAIL, email=email)
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Неверный пароль!'}, status=status.HTTP_400_BAD_REQUEST)
            except CrystalUser.DoesNotExist:
                return Response({'error': 'Такого пользователя не существует!'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenByVkCode(APIView):
    serializer_class = AuthCodeSerializer

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            409: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        },
    )
    def post(self, request):
        """ Need code from url parametr after redirecting from Oauth url authorization link"""
        serializer = self.serializer_class(data=request.data)
        vk_secret = settings.VK_OAUTH
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_vk_token(vk_secret, authorization_code)
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
                return Response(data={"token": token}, status=status.HTTP_200_OK)
            else:
                text = f"we have a problem with token response because {token_response.text}"
                return Response(data={'error': text}, status=status.HTTP_409_CONFLICT)
        return Response(data={'error': 'Invalid Date'}, status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenByPhone(APIView):
    serializer_class = AuthByPhoneSerializer

    @swagger_auto_schema(
        request_body=AuthByPhoneSerializer,
        responses={
            200: openapi.Response('Token', schema=openapi.Schema(type='object', properties={
                'token': openapi.Schema(type='string', description='Generated token'),
            })),
            400: openapi.Response('Error', schema=openapi.Schema(type='object', properties={
                'error': openapi.Schema(type='string', description='Details of the error'),
            })),
            201: openapi.Response('Details', schema=openapi.Schema(type='object', properties={
                'details': openapi.Schema(type='string', description='Details of the success'),
            })),
        },
    )
    def post(self, request):
        """only phone -> send code to phone number, create user/ 201
           phone + code (success) -> nothing/ token + 200:
           phone + code (wrong phone) -> create new user, send code to new number/ error 400
           phone + code (wrong code) -> nothing / error 400
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            if code:
                phone = serializer.validated_data.get('phone')
                user, created = CrystalUser.objects.get_or_create(identifier=phone, auth_type='phone')
                if created:
                    new_secure_code = get_phone_code_from_api(phone)
                    user.code = new_secure_code
                    user.save()
                    return Response(
                        data={'error': 'Cant to find user with that phone. Created new and sended code. Try again '
                                       'with new code'},
                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    saved_code = user.code
                    if saved_code == 'clear':
                        new_secure_code = get_phone_code_from_api(phone)
                        user.code = new_secure_code
                        user.save()
                        return Response({'error': 'No active code on this phone, sended new. Try again with new code'})

                    if str(code) == str(saved_code):
                        token, created = Token.objects.get_or_create(user=user)
                        user.code = 'clear'
                        user.save()
                        return Response(data={'token': token.key}, status=status.HTTP_200_OK)
                    else:
                        return Response(data={'error': 'Looks that it is a wrong code, try again'},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:
                phone = serializer.validated_data.get('phone')
                secure_code = get_phone_code_from_api(phone)
                user, created = CrystalUser.objects.get_or_create(identifier=phone, auth_type='phone')
                user.code = secure_code
                user.save()
                return Response(data={'details': 'we send code to phone number'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': f"Invalid Income Data {serializer.errors}"},
                            status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenByGoogleCode(APIView):
    serializer_class = AuthCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        google_secret = settings.GOOGLE_OAUTH
        if serializer.is_valid():
            authorization_code = serializer.validated_data.get('code')
            payload, token_url = create_payload_for_access_google_token(google_secret, authorization_code)
            token_response = requests.post(token_url, data=payload)
            if token_response.status_code == 200:
                access_token = token_response.json().get('id_token')
                try:
                    email, name = get_user_info(access_token)
                except Exception as er:
                    return Response(data={'error': f'Unexpected error in obtain user info with access token {er}'},
                                    status=status.HTTP_409_CONFLICT)

                user, was_born = CrystalUser.objects.create_user(identifier=email, auth_type='google')
                token, crafted = Token.objects.get_or_create(user=user)

                return Response(data={"result": "success", "token": token}, status=status.HTTP_200_OK)
            else:
                return Response(data={'error': f'cant to obtain google access token because {token_response.text}'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            errors = serializer.errors
            return Response(data={"error": f"Data invalid: {errors}"},
                            status=status.HTTP_400_BAD_REQUEST)


class CreateAuthLinks(APIView):
    @swagger_auto_schema(
        operation_description="Get OAuth links for Google and VK",
        manual_parameters=[],
        responses={200: OAuthUrlsSerializer},
    )
    def get(self, request):
        """
        Get OAuth links for Google and VK.
        """
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
        result = {
            'google_url': google_result,
            'vk_url': vk_result
        }
        serializer = OAuthUrlsSerializer(data=result)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    model_class = CrystalUser
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_description="Получение и изменение информации о залогиненном пользователе",
        methods=["PUT", "PATCH"],
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: ErrorSerializer,
        }
    )
    @swagger_auto_schema(method="GET", responses={
        200: UserSerializer,
        401: ErrorSerializer,
    })
    @action(detail=False, methods=['put', 'patch', 'get', 'delete'])
    def me(self, request):
        """Получить/Изменить/Удалить данные пользователя  (имя,фамилия, почта)"""
        if request.method == "GET":
            user = self.get_object()
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=200)
        elif request.method in ["PUT", "PATCH"]:
            user = self.get_object()
            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            user = self.get_object()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=PasswordSerializer,
        responses={
            200: SuccessSerializer,
            400: ErrorSerializer,
        }
    )
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Изменить пароль пользователя"""
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Пароль успешно изменён.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={
            201: openapi.Response('Пользователь создан', RegistrationSerializer),
            400: openapi.Response('Пользователь не создан')
        },
        operation_summary="Регистрация пользователя по паролю ( телефон или почта)",
        operation_description="Создает пользователя. Поля email или phone используются соответственно"
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def registration(self, request):
        """Зарегистрировать пользователя по паролю и Union[Телефон, Почта]"""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as er:
                if "UNIQUE" in str(er):
                    error_field = str(er).split(": ")[1].split(".")[1]
                    return Response(data={'errors': {error_field: ['Пользователь с такими данными уже существует']}},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(
                        data={'errors': {'non_field_errors': ["При создании пользователя произошла ошибка."]}},
                        status=status.HTTP_400_BAD_REQUEST)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class YandexAuthTokenAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = YandexAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = requests.get(
                'https://login.yandex.ru/info',
                headers={
                    "Authorization": f"OAuth {serializer.validated_data.get('token', '')}",
                },
                params={
                    'format': 'json',
                }
            )
            try:
                user_info = response.json()
                yandex_id = user_info.get('id')
                user, created = User.objects.get_or_create(yandex_id=yandex_id)
                user.first_name = user_info.get('first_name')
                user.last_name = user_info.get('last_name')
                user.email = user_info.get('default_email')
                user.auth_type = YANDEX
                user.phone = user_info.get('default_phone', {}).get('number')
                user.save()

                auth_token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": auth_token.key}, status=status.HTTP_200_OK)
            except Exception as e:
                Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
