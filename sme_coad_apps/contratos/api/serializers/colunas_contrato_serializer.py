from rest_framework import serializers

from ...models import ColunasContrato


class ColunasContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColunasContrato
        fields = ('usuario', 'colunas_array')
