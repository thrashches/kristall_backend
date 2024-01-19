from django.contrib import admin

from .models import RetailOffice


@admin.register(RetailOffice)
class RetailOfficeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'address',
        'phone',
        'working_hours',
    ]
