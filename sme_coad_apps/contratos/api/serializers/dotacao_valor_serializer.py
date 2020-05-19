from rest_framework import serializers

from ...models import DotacaoValor, Contrato


class DotacaoValorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = DotacaoValor
        fields = ('uuid', 'contrato', 'dotacao_orcamentaria', 'valor')


class DotacaoValorCreatorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = DotacaoValor
        fields = '__all__'
