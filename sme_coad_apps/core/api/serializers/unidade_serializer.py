from rest_framework import serializers

from ...models.unidade import Unidade


class UnidadeLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = ('uuid', 'codigo_eol', 'tipo_unidade', 'nome', 'logradouro', 'bairro')


class UnidadeSerializer(serializers.ModelSerializer):
    dre = UnidadeLookUpSerializer()

    class Meta:
        model = Unidade
        fields = '__all__'
