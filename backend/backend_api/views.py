from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authorization.auth_class import JWTTokenFromCookieUserAuthentication


class HelloWorldView(APIView):
    authentication_classes = [JWTTokenFromCookieUserAuthentication]

    def post(self, request):
        return Response({"hello": "world"})