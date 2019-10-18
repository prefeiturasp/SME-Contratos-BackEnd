from rest_framework import serializers

from ..serializers.divisao_serializer import DivisaoLookUpSerializer
from ...models import Nucleo


class NucleoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nucleo
        fields = ('id', 'sigla', 'nome')


class NucleoLookUpSerializer(serializers.ModelSerializer):
    divisao = DivisaoLookUpSerializer()

    class Meta:
        model = Nucleo
        fields = ('sigla', 'uuid', 'divisao')
