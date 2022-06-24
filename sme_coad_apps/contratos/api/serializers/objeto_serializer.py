from django.db import IntegrityError
from rest_framework import serializers

from ...models import Objeto


class ObjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objeto
        fields = ('nome', 'uuid')


class ObjetoLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objeto
        fields = ('nome', 'uuid', 'id')


class ObjetoCreateSerializer(serializers.Serializer):
    nome = serializers.CharField()

    def create(self, validated_data):
        validated_data['nome'] = validated_data['nome'].upper()
        try:
            objeto = Objeto.objects.create(**validated_data)

        except IntegrityError:
            raise serializers.ValidationError('Esta categoria de objeto já está cadastrada!')
        return objeto

    class Meta:
        model = Objeto
        fields = ('nome', 'uuid')
