from rest_framework import serializers
from authorization.models import CrystalUser
from cabinet.models import Basket


class CrystalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrystalUser
        fields = ('first_name', 'second_name', 'email')

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'