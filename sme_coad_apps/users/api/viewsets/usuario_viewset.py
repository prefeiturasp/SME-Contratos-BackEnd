from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.permissions.usuario_invalidado_permission import UsuarioInvalidadoPermission
from ..serializers.usuario_serializer import (UsuarioSerializer, UsuarioSerializerCreators)
from ...models import User


class UsuarioViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()

    def get_serializer_class(self):
        if not self.action in ['create', 'update', 'partial_update']:
            return UsuarioSerializerCreators
        return UsuarioSerializer

    @action(detail=True, url_path='troca-senha', methods=['patch'], permission_classes=[UsuarioInvalidadoPermission])
    def troca_senha(self, request, username):
        serialized = UsuarioSerializerCreators().validate(request.data)
        print(serialized)
        # if User.objects.update(**request.data):
        #     return Response({'detail': 'Usuário validado', 'status': status.HTTP_200_OK})
        # return Response({'detail': 'Error ao tentar trocar senha', 'status': status.HTTP_400_BAD_REQUEST})

