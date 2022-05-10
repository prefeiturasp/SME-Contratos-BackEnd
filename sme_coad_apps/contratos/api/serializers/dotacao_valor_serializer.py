from rest_framework import serializers

from ...models import Contrato, DotacaoValor
from ...models.dotacao_valor import DotacaoOrcamentaria


class DotacaoValorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = DotacaoValor
        fields = ('uuid', 'contrato', 'dotacao_orcamentaria', 'valor')


class DotacaoValorLookUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = DotacaoValor
        fields = ('uuid', 'dotacao_orcamentaria', 'valor')


class DotacaoValorCreatorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = DotacaoValor
        fields = '__all__'


class DotacaoOrcamentariaSerializer(serializers.ModelSerializer):
    numero_dotacao = serializers.ReadOnlyField()

    class Meta:
        model = DotacaoOrcamentaria
        fields = ('uuid', 'orgao', 'unidade', 'funcao', 'subfuncao',
                  'programa', 'projeto_atividade', 'conta_despesa', 'fonte', 'numero_dotacao')


class DotacaoOrcamentariaLookUpSerializer(serializers.ModelSerializer):
    numero_dotacao = serializers.ReadOnlyField()

    class Meta:
        model = DotacaoOrcamentaria
        fields = ('uuid', 'numero_dotacao')


class DotacaoOrcamentariaCreatorSerializer(serializers.ModelSerializer):
    orgao = serializers.CharField(required=True)
    unidade = serializers.CharField(required=True)
    funcao = serializers.CharField(required=True)
    subfuncao = serializers.CharField(required=True)
    programa = serializers.CharField(required=True)
    projeto_atividade = serializers.CharField(required=True)
    conta_despesa = serializers.CharField(required=True)
    fonte = serializers.CharField(required=True)

    class Meta:
        model = DotacaoOrcamentaria
        fields = '__all__'
