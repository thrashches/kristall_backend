from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authorization.models import CrystalUser, PHONE, MAIL


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
            'phone',
            'is_wholesale',
            'birthday',
            'company',
            'bonus_balance',
        ]
        read_only_fields = [
            'id',
            'auth_type',
            'identifier',
            'bonus_balance',
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CrystalUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_wholesale',
            'password',
            'password_confirm',
            'auth_type'
        ]

    def validate(self, data):
        email = data.get('email', None)
        phone = data.get('phone', None)
        auth_type = data.get('auth_type')
        if auth_type == PHONE and not phone:
            raise serializers.ValidationError("Поле телефон должно быть заполнено.")
        elif auth_type == MAIL and not email:
            raise serializers.ValidationError("Поле почта должно быть заполнено.")
        return data

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_password_confirm(self, value):
        password = self.initial_data.get('password')
        if password != value:
            raise serializers.ValidationError("Пароли не совпадают.")
        return value

    def create(self, validated_data):
        """90% это костыль и можно как то сделать без этого"""
        validated_data.pop('password_confirm', None)
        user = CrystalUser(**validated_data)
        password = validated_data.pop('password', None)

        if password is not None:
            user.set_password(password)
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class YandexAuthSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)
