from rest_framework import serializers
from .models import RetailOffice


class RetailOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailOffice
        fields = '__all__'
