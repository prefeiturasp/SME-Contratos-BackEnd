from django.contrib.auth import get_user_model
from rest_framework import serializers

from ....contratos.models.contrato import ContratoUnidade, FiscaisUnidade
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer

user_model = get_user_model()


class FiscalContratoUnidadeSerializer(serializers.ModelSerializer):
    contrato_unidade = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=ContratoUnidade.objects.all()
    )
    fiscal = UsuarioLookUpSerializer()

    class Meta:
        model = FiscaisUnidade
        fields = '__all__'


class FiscalContratoUnidadeSerializerCreate(serializers.ModelSerializer):
    contrato_unidade = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=ContratoUnidade.objects.all()
    )
    fiscal = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=user_model.objects.all()
    )

    class Meta:
        model = FiscaisUnidade
        fields = '__all__'
