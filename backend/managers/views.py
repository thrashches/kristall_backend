from rest_framework import viewsets, mixins, permissions

from .models import ManagerFeedback
from .serializers import ManagerFeedbackSerializer


class ManagerFeedbackViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ManagerFeedbackSerializer
    queryset = ManagerFeedback.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
