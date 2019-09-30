from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.usuario_serializer import (UsuarioSerializer, UsuarioSerializerCreators)

user_model = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UsuarioSerializer
        elif self.action == 'list':
            return UsuarioSerializer
        else:
            return UsuarioSerializerCreators

    @action(detail=True, url_path='primeiro-acesso', methods=['get'], permission_classes=[AllowAny])
    def primeiro_acesso(self, request, username=None):
        serializer = UsuarioSerializer().validate_validado(username)
        if serializer:
            return Response({'detail': 'Pode acessar o sistema', 'alterar': False}, status=status.HTTP_200_OK)
        return Response({'detail': 'Deve alterar a senha padrão', 'alterar': True}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, url_path='troca-senha', methods=['patch'], permission_classes=[AllowAny])
    def troca_senha(self, request, username):
        data = request.data
        validated_data = UsuarioSerializerCreators().validate(data)
        usuario = user_model.objects.get(username=username)
        UsuarioSerializerCreators().update(usuario, validated_data)
        return Response({'detail': 'Usuário validado', 'status': status.HTTP_200_OK})
