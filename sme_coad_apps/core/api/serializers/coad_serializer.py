from rest_framework import serializers

from .coad_assessor_serializer import CoadAssessorSerializer
from ...models import Coad


class CoadSerializer(serializers.ModelSerializer):
    assessores = CoadAssessorSerializer(many=True)

    class Meta:
        model = Coad
        fields = '__all__'


class CoadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coad
        fields = ('id', 'coordenador')
