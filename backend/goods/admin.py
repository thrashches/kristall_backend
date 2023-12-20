from django.contrib import admin
from goods.models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'visible', 'is_new')
    list_filter = ('visible', 'is_new', 'category')
    search_fields = ('title', 'description')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_file', 'visible')
    list_filter = ('visible',)
    search_fields = ('product__title',)