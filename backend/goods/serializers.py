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
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj: Product):
        if obj.images.exists():
            image = obj.images.first()
            serializer = SingleImageSerializer(instance=image, context=self.context)
            return serializer.data.get("image_file")
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
