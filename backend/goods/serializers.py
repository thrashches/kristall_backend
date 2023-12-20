from rest_framework import serializers
from goods.models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    image_file = serializers.SerializerMethodField()

    def get_image_file(self, obj):
        return self.context['request'].build_absolute_uri(obj.image_file.url).replace('http://', 'https://')

    class Meta:
        model = ProductImage
        fields = '__all__'
