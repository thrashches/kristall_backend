from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

def home(request):
    return HttpResponse("Welcome to the homepage!")

class HelloWorldView(APIView):
    def get(self, request):
        return Response({"hello": "world"})
