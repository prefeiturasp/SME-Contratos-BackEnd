from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...models import Servidor
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer

user_model = get_user_model()


class ServidorSerializer(serializers.ModelSerializer):
    servidor = UsuarioLookUpSerializer()

    class Meta:
        model = Servidor
        fields = ('id', 'servidor', 'nucleo')


class ServidorCreateSerializer(serializers.ModelSerializer):
    servidor = serializers.SlugRelatedField(
        slug_field='username',
        required=False,
        queryset=user_model.objects.all()
    )

    class Meta:
        model = Servidor
        fields = ('id', 'servidor', 'nucleo')
