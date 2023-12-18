from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TestT(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content


                        )