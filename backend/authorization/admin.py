from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CrystalUser


class CrystalUserAdmin(UserAdmin):
    list_display = ('id', 'username','is_wholesale', 'email', 'auth_type', 'identifier')
    fieldsets = (
        (None, {"fields": (
            "username", "password",
            "auth_type", "code",'is_wholesale'
        )}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(CrystalUser, CrystalUserAdmin)
