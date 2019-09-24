from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from sme_coad_apps.core.permissions.usuario_invalidado_permission import UsuarioInvalidadoPermission
from ..serializers.usuario_serializer import (UsuarioSerializer, UsuarioSerializerCreators)
from ...models import User


class UsuarioViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UsuarioSerializer
        elif self.action == 'list':
            return UsuarioSerializer
        else:
            return UsuarioSerializerCreators

    @action(detail=True, url_path='troca-senha', methods=['patch'], permission_classes=[UsuarioInvalidadoPermission])
    def troca_senha(self, request, username):
        usuario = request.user
        data = request.data
        UsuarioSerializerCreators().validate(data)
        usuario.set_password(data.get('password'))
        usuario.validado = True
        usuario.save()
        return Response({'detail': 'Usuário validado', 'status': status.HTTP_200_OK})

