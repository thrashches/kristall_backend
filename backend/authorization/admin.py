from django.contrib import admin
from .models import CrystalUser
from django.contrib.auth.hashers import make_password


class CrystalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'auth_type', 'identifier')
    fields = ('auth_type', 'identifier', 'password')

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password = make_password(obj.password)
        obj.save()


admin.site.register(CrystalUser, CrystalUserAdmin)
