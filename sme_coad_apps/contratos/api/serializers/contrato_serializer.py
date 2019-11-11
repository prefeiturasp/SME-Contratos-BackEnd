from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..validations.contrato_validations import gestor_e_suplente_devem_ser_diferentes
from ...api.serializers.empresa_serializer import EmpresaLookUpSerializer
from ...api.serializers.tipo_servico_serializer import TipoServicoSerializer
from ...models import Contrato, Empresa
from ...models.tipo_servico import TipoServico
from ....core.api.serializers.nucleo_serializer import NucleoLookUpSerializer
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
    suplente = UsuarioLookUpSerializer()
    total_mensal = serializers.SerializerMethodField('get_total_mensal')
    row_index = serializers.SerializerMethodField('get_row_index')
    dias_para_o_encerramento = serializers.SerializerMethodField('get_dias_para_o_encerramento')

    def get_data_encerramento(self, obj):
        return obj.data_encerramento

    def get_total_mensal(self, obj):
        return obj.total_mensal

    def get_row_index(self, obj):
        self.CONT += 1
        return self.CONT

    def get_dias_para_o_encerramento(self, obj):
        return obj.dias_para_o_encerramento

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

    def validate(self, attrs):
        gestor_e_suplente_devem_ser_diferentes(attrs.get('gestor'), attrs.get('suplente'))
        return attrs

    class Meta:
        model = Contrato
        exclude = ('id',)


class ContratoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = ('uuid', 'termo_contrato', 'gestor', 'suplente', 'criado_em')
