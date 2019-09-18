from rest_framework import viewsets

from ..serializers.usuario_serializer import UsuarioSerializer
from ...models import User


class UsuarioViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
