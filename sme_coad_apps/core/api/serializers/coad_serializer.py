from rest_framework import serializers

from .coad_assessor_serializer import CoadAssessorSerializer
from ...models import Coad
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer


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
