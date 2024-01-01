from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    errors = serializers.CharField(read_only=True)


class SuccessSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
