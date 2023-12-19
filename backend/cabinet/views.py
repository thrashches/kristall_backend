from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from authorization.models import CrystalUser
from cabinet.models import Basket
from cabinet.serializers import CrystalUserSerializer


class basket(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BascketSerializer


class CabinetUserViewSet(viewsets.ModelViewSet):
    queryset = CrystalUser.objects.all()
    serializer_class = CrystalUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CrystalUser.objects.filter(pk=user.pk)
