from rest_framework import viewsets

from sme_coad_apps.users.api.serializers.usuario_serializer import UsuarioSerializer
from sme_coad_apps.users.models import User


class UsuarioViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
