from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # Генерация slug автоматически

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    menu = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    weight = models.FloatField()
    energy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='product_images/')
    visible = models.BooleanField(default=True)
