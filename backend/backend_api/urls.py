from django.urls import path
from .views import HelloWorldView
from django.http import HttpResponse


def home(request):
    return HttpResponse("Welcome to the homepage!")


urlpatterns = [
    path("", home),
    path("hello", HelloWorldView.as_view(), name='hello_world'),
]
