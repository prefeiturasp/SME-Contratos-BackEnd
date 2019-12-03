from rest_framework import serializers

from ..serializers.fiscal_contrato_unidade_serializer import FiscalContratoUnidadeSerializer
from ....contratos.models.contrato import ContratoUnidade, Contrato
from ....core.api.serializers.unidade_serializer import UnidadeSerializer, UnidadeLookUpSerializer
from ....core.models.unidade import Unidade


class ContratoUnidadeSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    unidade = UnidadeLookUpSerializer()

    class Meta:
        model = ContratoUnidade
        fields = '__all__'


class ContratoUnidadeCreatorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    unidade = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Unidade.objects.all()
    )

    class Meta:
        model = ContratoUnidade
        fields = '__all__'


class ContratoUnidadeLookUpSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    unidade = UnidadeSerializer()
    fiscais = FiscalContratoUnidadeSerializer(many=True)

    class Meta:
        model = ContratoUnidade
        fields = '__all__'
