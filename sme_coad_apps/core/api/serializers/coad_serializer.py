from rest_framework import serializers

from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer
from ...models import Coad
from .coad_assessor_serializer import CoadAssessorSerializer


class CoadSerializer(serializers.ModelSerializer):
    assessores = CoadAssessorSerializer(many=True)
    coordenador = UsuarioLookUpSerializer()

    class Meta:
        model = Coad
        fields = '__all__'


class CoadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coad
        fields = ('id', 'coordenador')
