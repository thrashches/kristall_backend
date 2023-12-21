from rest_framework import serializers

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


class ChangeUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrystalUser
        fields = ['first_name', 'last_name', 'email']

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
        }

class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField

