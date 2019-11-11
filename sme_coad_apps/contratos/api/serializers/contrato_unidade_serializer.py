from rest_framework import serializers

from ....contratos.models.contrato import ContratoUnidade, Contrato
from ....core.models.unidade import Unidade


class ContratoUnidadeSerializer(serializers.ModelSerializer):
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