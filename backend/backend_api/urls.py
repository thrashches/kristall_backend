from django.urls import path
from .views import TestT


urlpatterns = [
    path("hello/", TestT.as_view(), name='hello_world'),
]
