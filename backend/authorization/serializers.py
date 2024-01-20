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
            'telephone'
        ]
        read_only_fields = [
            'id',
            'auth_type',
            'identifier',
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    # Определяем поля для записи данных
    email = serializers.CharField(required=False, allow_blank=True)
    telephone = serializers.CharField(required=False, allow_blank=True)
    is_wholesale = serializers.BooleanField()

    class Meta:
        model = CrystalUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'telephone',
            'is_wholesale',
            'auth_type',
            'identifier',
            'id',
        ]
        read_only_fields = [
            'id',
            'auth_type',
            'identifier',
            'auth_type'
        ]

    def validate(self, data):
        email = data.get('email', None)
        telephone = data.get('telephone', None)
        if not email and not telephone:
            raise serializers.ValidationError("Поле 'email' или 'telephone' должно быть заполнено.")
        if email and telephone:
            raise serializers.ValidationError("Только одно из полей 'email' или 'telephone' может быть заполнено.")
        if email:
            data['auth_type'] = MAIL
        elif telephone:
            data['auth_type'] = PHONE
        return data


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value
