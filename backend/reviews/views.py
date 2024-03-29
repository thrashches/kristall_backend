from rest_framework import viewsets, mixins

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.filter(published=True)
    serializer_class = ReviewSerializer
    pagination_class = None
