from django.contrib import admin
from .models import CrystalUser


class CrystalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'auth_type', 'username')
    search_fields = ('email', 'auth_type', 'username')


admin.site.register(CrystalUser, CrystalUserAdmin)
