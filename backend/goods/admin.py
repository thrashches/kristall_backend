import os

from django.contrib import admin
from goods.models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'price', 'visible', 'is_new')
    list_filter = ('visible', 'is_new', 'menu')
    search_fields = ('title', 'description')

    def menu(self, obj):
        return obj.menu.name

    menu.short_description = 'Category'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_file', 'visible')
    list_filter = ('visible',)
    search_fields = ('product__title',)

    def delete_model(self, request, obj):
        file_path = obj.image.path
        obj.delete()
        if file_path and os.path.isfile(file_path):
            os.remove(file_path)