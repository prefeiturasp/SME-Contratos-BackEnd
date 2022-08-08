from rest_framework import fields, serializers

from ...models.aditamento import Aditamento
from ...models.contrato import Contrato
from ..validations.contrato_validations import campo_nao_pode_ser_nulo


class AditamentoSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = Aditamento
        exclude = ('id',)


class AditamentoCreateSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    objeto_aditamento = fields.MultipleChoiceField(choices=Aditamento.OBJETO_CHOICES)

    def validate(self, attrs):
        objetos_aditamento = attrs['objeto_aditamento']
        if ('PRORROGACAO_VIGENCIA_CONTRATUAL' or 'MODIFICACAO_PROJETO_ESPECIFICACOES' or
                'MODIFICACAO_VALOR_CONTRATUAL') in objetos_aditamento:
            campo_nao_pode_ser_nulo(attrs.get('valor_mensal_atualizado', None),
                                    mensagem='Valor mensal atualizado obrigatório.')
            campo_nao_pode_ser_nulo(attrs.get('valor_total_atualizado', None),
                                    mensagem='Valor total Atualizado obrigatório')
            campo_nao_pode_ser_nulo(attrs.get('data_inicial', None),
                                    mensagem='Data inicial obrigatório')
            campo_nao_pode_ser_nulo(attrs.get('data_final', None),
                                    mensagem='Data final obrigatório')
            if 'MODIFICACAO_VALOR_CONTRATUAL' in objetos_aditamento:
                campo_nao_pode_ser_nulo(attrs.get('valor_aditamento', None),
                                        mensagem='Valor do aditamento obrigatório.')

        return attrs

    class Meta:
        model = Aditamento
        exclude = ('id',)
