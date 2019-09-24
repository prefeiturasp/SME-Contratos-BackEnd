from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.senha_serializer import EsqueciMinhaSenhaSerializer, RedefinirSenhaSerializer

user_model = get_user_model()


class EsqueciMinhaSenhaViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = user_model.objects.all()
    serializer_class = EsqueciMinhaSenhaSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        usuario = request.user
        EsqueciMinhaSenhaSerializer().validate(request.data)
        usuario.is_active = False
        usuario.save()
        return Response({'status': 200, 'content': 'Esqueceu sua sennha'})


class RedefinirSenhaViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = user_model.objects.all()
    serializer_class = RedefinirSenhaSerializer
    permission_classes = [AllowAny]
