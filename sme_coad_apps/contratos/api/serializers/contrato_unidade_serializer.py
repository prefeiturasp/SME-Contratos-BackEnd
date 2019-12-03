from rest_framework import serializers

from ..serializers.fiscal_contrato_unidade_serializer import FiscalContratoUnidadeSerializer, \
    FiscalContratoUnidadeSerializerCreate
from ....contratos.models.contrato import ContratoUnidade, Contrato
from ....core.api.serializers.unidade_serializer import UnidadeSerializer, UnidadeLookUpSerializer
from ....core.helpers.update_instance_from_dict import update_instance_from_dict
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

    fiscais = FiscalContratoUnidadeSerializerCreate(many=True)

    def create(self, validated_data):
        fiscais = validated_data.pop('fiscais')

        fiscais_lista = []
        for fiscal in fiscais:
            fiscais_object = FiscalContratoUnidadeSerializerCreate(
            ).create(fiscal)
            fiscais_lista.append(fiscais_object)
        contrato_unidade = ContratoUnidade.objects.create(**validated_data)
        contrato_unidade.fiscais.set(fiscais_lista)

        return contrato_unidade

    def update(self, instance, validated_data):
        fiscais_json = validated_data.pop('fiscais')
        instance.fiscais.all().delete()

        fiscais_lista = []
        for fiscal_json in fiscais_json:
            fiscais_object = FiscalContratoUnidadeSerializerCreate(
            ).create(fiscal_json)
            fiscais_lista.append(fiscais_object)

        update_instance_from_dict(instance, validated_data)
        instance.fiscais.set(fiscais_lista)
        instance.save()

        return instance

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
