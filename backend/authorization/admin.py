from django.contrib import admin
from .models import CrystalUser


class CrystalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'auth_type', 'username')  # добавьте остальные поля модели
    search_fields = ('email', 'auth_type', 'username')  # добавьте поля для поиска


admin.site.register(CrystalUser, CrystalUserAdmin)
