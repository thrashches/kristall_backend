from rest_framework import serializers


class AuthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    scope = serializers.CharField()
    authuser = serializers.CharField()
    prompt = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
