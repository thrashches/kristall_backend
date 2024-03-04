from rest_framework import serializers
from .models import ManagerFeedback


class ManagerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerFeedback
        exclude = [
            'processed',
        ]
