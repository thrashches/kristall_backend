from rest_framework import serializers


class AuthPswSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
