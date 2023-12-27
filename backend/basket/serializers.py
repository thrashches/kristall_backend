from rest_framework import serializers

from basket.models import Order

"""Версия без ModelSerializer"""


class orderIncomeItemSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()


class orderIncomeSerializer(serializers.Serializer):
    items = orderIncomeItemSerializer(many=True)
    products_pk = serializers.SerializerMethodField(required=False)
    items_dict = serializers.SerializerMethodField(required=False)

    def get_products_pk(self, obj):
        items = self.validated_data['items']
        product_pk = []
        for item in items:
            product_pk.append(item.get('product'))
        return product_pk

    def get_items_dict(self, obj):
        items = self.validated_data['items']
        items_dict = {}
        for item in items:
            pk = item.get('product')
            items_dict[pk] = item.get('quantity')
        return items_dict


class orderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()  # products id
    name = serializers.IntegerField()
    price = serializers.IntegerField()
    image = serializers.IntegerField(required=False)


class orderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.IntegerField()
    date = serializers.DateField
    price = serializers.IntegerField()
    status = serializers.CharField()
    items = orderItemSerializer(many=True)



