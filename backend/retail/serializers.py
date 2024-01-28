from rest_framework import serializers

from .models import RetailOffice


class RetailOfficeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = RetailOffice
        fields = '__all__'

    def get_image(self, obj: RetailOffice):
        return obj.image.url
