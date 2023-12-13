from django.urls import path
from .views import HelloWorldView, home


urlpatterns = [
    path("", home),
    path("hello", HelloWorldView.as_view(), name='hello_world'),
]
