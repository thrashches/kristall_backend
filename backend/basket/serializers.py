from rest_framework import serializers

"""Версия без ModelSerializer"""


class orderIncomeItemSerializer(serializers.Serializer):
    prodict = serializers.IntegerField()
    quantity = serializers.IntegerField()


class orderIncomeSerializer(serializers.Serializer):
    items = orderIncomeItemSerializer(many=True)
    products_pk = serializers.


class orderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.IntegerField()
    price = serializers.IntegerField()
    image = serializers.IntegerField()


class orderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.IntegerField()
    date = serializers.DateField
    price = serializers.IntegerField()
    status = serializers.CharField()
    items = orderItemSerializer(many=True)