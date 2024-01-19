from rest_framework import viewsets, permissions
from .models import RetailOffice
from .serializers import RetailOfficeSerializer


class RetailOfficeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RetailOffice.objects.all()
    serializer_class = RetailOfficeSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
