from rest_framework import serializers
from goods.models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class SingleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'image_file',
        ]


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    energy = serializers.DecimalField(decimal_places=0, max_digits=10)
    weight = serializers.DecimalField(decimal_places=0, max_digits=10)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Product
        fields = '__all__'
        ref_name = "ProductSerializer"

    def get_image(self, obj: Product):
        if obj.images.exists():
            image = obj.images.first()
            return image.image_file.url
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    image_file = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = '__all__'

    def get_image_file(self, obj: ProductImage):
        return obj.image_file.url
