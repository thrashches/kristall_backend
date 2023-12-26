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

    def validate(self, data):
        fields_to_check = ['first_name', 'last_name', 'email']
        non_empty_fields = [field for field in fields_to_check if data.get(field)]
        if not non_empty_fields:
            raise serializers.ValidationError("At least one field should not be empty.")
        return data

    class Meta:
        model = CrystalUser
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
        }


class ChangeUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)


class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField
