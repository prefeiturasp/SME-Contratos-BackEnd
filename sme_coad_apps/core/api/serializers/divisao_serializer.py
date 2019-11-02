from rest_framework import serializers

from ...models import Divisao
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer


class DivisaoSerializer(serializers.ModelSerializer):
    diretor = UsuarioLookUpSerializer()
    suplente_diretor = UsuarioLookUpSerializer()

    class Meta:
        model = Divisao
        fields = '__all__'


class DivisaoSerializerCreator(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = '__all__'


class DivisaoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = ('sigla', 'uuid')
