from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authorization.models import CrystalUser


class AuthPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class AuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class AuthByPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField(allow_null=True, required=False)


class OAuthUrlsSerializer(serializers.Serializer):
    google_url = serializers.CharField()
    vk_url = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrystalUser
        fields = [
            'first_name',
            'last_name',
            'email',  # FIXME: Сделать проверку почты при смене
            'auth_type',
            'identifier',
            'id',
        ]
        read_only_fields = [
            'id',
            'auth_type',
            'identifier',
        ]


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value
