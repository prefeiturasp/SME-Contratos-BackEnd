from rest_framework import serializers

from ...models import Contrato, DotacaoValor
from ...models.dotacao_valor import DotacaoOrcamentaria, Empenho


class EmpenhoLookUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empenho
        fields = ('uuid', 'numero', 'valor_previsto')


class EmpenhoCreatorSerializer(serializers.ModelSerializer):
    dotacao_valor = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=DotacaoValor.objects.all()
    )
    numero = serializers.CharField(required=True)
    valor_previsto = serializers.DecimalField(max_digits=15, decimal_places=2, required=True)

    class Meta:
        model = Empenho
        fields = '__all__'


class DotacaoOrcamentariaLookUpSerializer(serializers.ModelSerializer):
    numero_dotacao = serializers.ReadOnlyField()

    class Meta:
        model = DotacaoOrcamentaria
        fields = ('uuid', 'numero_dotacao')


class DotacaoValorSerializer(serializers.ModelSerializer):
    dotacao_orcamentaria = DotacaoOrcamentariaLookUpSerializer()
    empenhos = EmpenhoLookUpSerializer(many=True, required=False)

    class Meta:
        model = DotacaoValor
        fields = ('uuid', 'dotacao_orcamentaria', 'valor', 'empenhos')


class DotacaoValorLookUpSerializer(serializers.ModelSerializer):
    dotacao_orcamentaria = DotacaoOrcamentariaLookUpSerializer()

    class Meta:
        model = DotacaoValor
        fields = ('uuid', 'dotacao_orcamentaria', 'valor')


class DotacaoValorCreatorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Contrato.objects.all()
    )
    dotacao_orcamentaria = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=DotacaoOrcamentaria.objects.all()
    )
    valor = serializers.DecimalField(max_digits=15, decimal_places=2, required=True)
    empenhos = EmpenhoLookUpSerializer(many=True, required=False)

    def create(self, validated_data):
        empenhos = validated_data.pop('empenhos', [])
        dotacao_valor = DotacaoValor.objects.create(**validated_data)
        for empenho in empenhos:
            empenho['dotacao_valor'] = dotacao_valor
            EmpenhoCreatorSerializer().create(empenho)

        return dotacao_valor

    class Meta:
        model = DotacaoValor
        fields = ('uuid', 'contrato', 'dotacao_orcamentaria', 'valor', 'empenhos')


class DotacaoOrcamentariaSerializer(serializers.ModelSerializer):
    numero_dotacao = serializers.ReadOnlyField()

    class Meta:
        model = DotacaoOrcamentaria
        fields = ('uuid', 'orgao', 'unidade', 'funcao', 'subfuncao',
                  'programa', 'projeto_atividade', 'conta_despesa', 'fonte', 'numero_dotacao')


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
