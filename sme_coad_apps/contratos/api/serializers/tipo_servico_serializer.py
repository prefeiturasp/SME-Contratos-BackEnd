from django.db import IntegrityError
from rest_framework import serializers

from ...models import TipoServico


class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = ('nome', 'uuid')


class TipoServicoLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = ('nome', 'uuid', 'id')


class TipoServicoCreateSerializer(serializers.Serializer):
    nome = serializers.CharField()

    def create(self, validated_data):
        validated_data['nome'] = validated_data['nome'].upper()
        try:
            tipo_servico = TipoServico.objects.create(**validated_data)

        except IntegrityError:
            raise serializers.ValidationError('Esta categoria de objeto já está cadastrada!')
        return tipo_servico

    class Meta:
        model = TipoServico
        fields = ('nome', 'uuid')
