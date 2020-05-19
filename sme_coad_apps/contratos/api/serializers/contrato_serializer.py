from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..validations.contrato_validations import gestor_e_suplente_devem_ser_diferentes
from ...api.serializers.empresa_serializer import EmpresaLookUpSerializer
from ...api.serializers.tipo_servico_serializer import TipoServicoSerializer
from ...models import Contrato, Empresa, FiscalLote
from ...models.contrato import Lote
from ...models.tipo_servico import TipoServico
from ....core.api.serializers.nucleo_serializer import NucleoLookUpSerializer
from ....core.helpers.update_instance_from_dict import update_instance_from_dict
from ....core.models import Unidade
from ....core.models.nucleo import Nucleo
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer
from ....users.models import User

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
    total_mensal = serializers.SerializerMethodField('get_total_mensal')
    row_index = serializers.SerializerMethodField('get_row_index')
    dias_para_o_encerramento = serializers.SerializerMethodField('get_dias_para_o_encerramento')
    dres = serializers.SerializerMethodField('get_dres')

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
    unidades_selecionadas = serializers.ListField(required=False)

    def validate(self, attrs):
        gestor_e_suplente_devem_ser_diferentes(attrs.get('gestor'), attrs.get('suplente'))
        return attrs

    def update(self, instance, validated_data):
        unidades_selecionadas = validated_data.pop('unidades_selecionadas', [])
        instance.lotes.all().delete()
        update_instance_from_dict(instance, validated_data, save=True)

        for unidade_selecionada in unidades_selecionadas:
            lote = unidade_selecionada.get('lote')
            if instance.lotes.filter(nome=lote, contrato=instance).exists():
                lote = instance.lotes.get(nome=lote, contrato=instance)
            else:
                lote = Lote(nome=lote, contrato=instance)
                lote.save()
            unidade_json = unidade_selecionada.get('unidade')
            if Unidade.objects.filter(codigo_eol=unidade_json.get('cd_equipamento')).exists():
                unidade = Unidade.objects.get(codigo_eol=unidade_json.get('cd_equipamento'))
            else:
                unidade = Unidade(
                    equipamento=Unidade.get_equipamento_from_unidade(unidade_json),
                    tipo_unidade=unidade_json.get('tp_unidade_escolar'),
                    codigo_eol=unidade_json.get('cd_equipamento'),
                    nome=unidade_json.get('nm_equipamento'),
                    logradouro=unidade_json.get('logradouro'),
                    bairro=unidade_json.get('bairro')
                )
                unidade.save()
            if not FiscalLote.objects.filter(lote=lote).exists():
                usuario = User.objects.get(username=unidade_selecionada.get('rf_fiscal'))
                fiscal_lote = FiscalLote(lote=lote, fiscal=usuario, tipo_fiscal=FiscalLote.FISCAL_TITULAR)
                fiscal_lote.save()
                for suplente in unidade_selecionada.get('suplentes'):
                    usuario = User.objects.get(username=suplente.get('rf'))
                    suplente_lote = FiscalLote(lote=lote, fiscal=usuario)
                    suplente_lote.save()
            lote.unidades.add(unidade)
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
