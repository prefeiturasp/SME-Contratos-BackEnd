from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.senha_serializer import (EsqueciMinhaSenhaSerializer,
                                            RedefinirSenhaSerializer,
                                            RedefinirSenhaSerializerCreator)

user_model = get_user_model()


class EsqueciMinhaSenhaViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = user_model.objects.all()
    permission_classes = [AllowAny]
    serializer_class = EsqueciMinhaSenhaSerializer


class RedefinirSenhaViewSet(viewsets.ModelViewSet):
    lookup_field = 'hash_redefinicao'
    queryset = user_model.objects.filter(username='123456')
    serializer_class = RedefinirSenhaSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return RedefinirSenhaSerializer
        elif self.action == 'retrieve':
            return RedefinirSenhaSerializer
        else:
            return RedefinirSenhaSerializerCreator

    def retrieve(self, request, hash_redefinicao=None):
        RedefinirSenhaSerializer().validate({'hash_redefinicao': hash_redefinicao})
        return Response({'detail': hash_redefinicao}, status=200)

    def create(self, request):
        serialize = RedefinirSenhaSerializerCreator()
        validated_data = serialize.validate(request.data)
        usuario = user_model.objects.get(hash_redefinicao=validated_data.get('hash_redefinicao'))
        serialize.update(usuario, validated_data)
        return Response({'detail': 'Senha redefinida com sucesso'}, status=200)
