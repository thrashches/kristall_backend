from django.contrib import admin

from .models import ManagerFeedback


@admin.register(ManagerFeedback)
class ManagerFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'created_at',
        'processed',
    ]

    list_editable = [
        'processed',
    ]
