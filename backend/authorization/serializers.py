from rest_framework import serializers


class AuthPswSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class AuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class ResultResponse(serializers.Serializer):
    result = serializers.CharField()
    details = serializers.CharField()


class AuthByPhone(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(allow_null=True, required=False)
