from rest_framework import serializers

from ....contratos.models.contrato import ContratoUnidade, FiscaisUnidade
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer


class FiscalContratoUnidadeSerializer(serializers.ModelSerializer):
    contrato_unidade = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=ContratoUnidade.objects.all()
    )
    fiscal = UsuarioLookUpSerializer()

    class Meta:
        model = FiscaisUnidade
        fields = '__all__'
