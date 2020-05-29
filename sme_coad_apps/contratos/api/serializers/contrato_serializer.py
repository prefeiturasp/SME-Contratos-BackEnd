from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..validations.contrato_validations import gestor_e_suplente_devem_ser_diferentes
from ...api.serializers.empresa_serializer import EmpresaLookUpSerializer
from ...api.serializers.tipo_servico_serializer import TipoServicoSerializer
from .dotacao_valor_serializer import DotacaoValorLookUpSerializer
from ...models import Contrato, Empresa, DotacaoValor
from ...models.tipo_servico import TipoServico
from ....core.api.serializers.nucleo_serializer import NucleoLookUpSerializer
from ....core.api.serializers.edital_serializer import EditalLookUpSerializer
from ....core.helpers.update_instance_from_dict import update_instance_from_dict
from ....core.models.nucleo import Nucleo
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer

user_model = get_user_model()


class ContratoSerializer(serializers.ModelSerializer):
    CONT = 0
    data_encerramento = serializers.SerializerMethodField('get_data_encerramento')
    tipo_servico = TipoServicoSerializer()
    empresa_contratada = EmpresaLookUpSerializer()
    nucleo_responsavel = NucleoLookUpSerializer()
    gestor = UsuarioLookUpSerializer()
    coordenador = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=user_model.objects.all()
    )
    suplente = UsuarioLookUpSerializer()
    edital = EditalLookUpSerializer()
    total_mensal = serializers.SerializerMethodField('get_total_mensal')
    row_index = serializers.SerializerMethodField('get_row_index')
    dias_para_o_encerramento = serializers.SerializerMethodField('get_dias_para_o_encerramento')
    dres = serializers.SerializerMethodField('get_dres')
    # dotacoes = DotacaoValorLookUpSerializer(many=True)
    dotacoes_orcamentarias = DotacaoValorLookUpSerializer(many=True, source='dotacoes')

    def get_data_encerramento(self, obj):
        return obj.data_encerramento

    def get_total_mensal(self, obj):
        return obj.total_mensal

    def get_row_index(self, obj):
        self.CONT += 1
        return self.CONT

    def get_dias_para_o_encerramento(self, obj):
        return obj.dias_para_o_encerramento

    def get_dres(self, obj):
        return obj.dres

    class Meta:
        model = Contrato
        fields = '__all__'


class ContratoCreateSerializer(serializers.ModelSerializer):
    tipo_servico = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=TipoServico.objects.all()
    )
    nucleo_responsavel = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Nucleo.objects.all()
    )
    empresa_contratada = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Empresa.objects.all()
    )
    coordenador = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=user_model.objects.all()
    )
    gestor = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=user_model.objects.all()
    )
    suplente = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=user_model.objects.all()
    )
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=user_model.objects.all()
    )
    dotacoes = DotacaoValorLookUpSerializer(many=True, required=False)
    dotacoes_orcamentarias = serializers.ListField(required=False)

    def validate(self, attrs):
        gestor_e_suplente_devem_ser_diferentes(attrs.get('gestor'), attrs.get('suplente'))
        return attrs

    def update(self, instance, validated_data):
        dotacoes = validated_data.pop('dotacoes_orcamentarias', [])
        instance.dotacoes.all().delete()
        update_instance_from_dict(instance, validated_data, save=True)
        for dotacao in dotacoes:
            dotacao_valor = DotacaoValor(
                contrato=instance,
                dotacao_orcamentaria=dotacao.get('dotacao_orcamentaria', ''),
                valor=dotacao.get('valor', '')
            )
            dotacao_valor.save()
        return instance

    class Meta:
        model = Contrato
        exclude = ('id',)


class ContratoLookUpSerializer(serializers.ModelSerializer):
    gestor = UsuarioLookUpSerializer()
    suplente = UsuarioLookUpSerializer()

    class Meta:
        model = Contrato
        fields = ('uuid', 'termo_contrato', 'gestor', 'coordenador', 'suplente', 'alterado_em')
