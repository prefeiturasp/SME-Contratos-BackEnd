from rest_framework import fields, serializers

from ...models.aditamento import Aditamento
from ...models.contrato import Contrato
from ..validations.contrato_validations import validacao_objetos_aditamento


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
        validacao_objetos_aditamento(attrs)
        return attrs

    class Meta:
        model = Aditamento
        exclude = ('id',)
