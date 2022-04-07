from django.contrib.auth import get_user_model
from rest_framework import serializers

from ....core.api.serializers.nucleo_serializer import NucleoLookUpSerializer
from ....core.api.serializers.unidade_serializer import UnidadeSerializer
from ....core.helpers.update_instance_from_dict import update_instance_from_dict
from ....core.models import Nucleo, Unidade
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer
from ....users.models import User
from ...api.serializers.edital_serializer import EditalListaSerializer
from ...api.serializers.empresa_serializer import EmpresaLookUpSerializer
from ...api.serializers.tipo_servico_serializer import TipoServicoLookupSerializer
from ...models import Contrato, DotacaoValor, Empresa, FiscalLote, Lote
from ...models.edital import Edital
from ...models.tipo_servico import TipoServico
from ..validations.contrato_validations import gestor_e_suplente_devem_ser_diferentes
from .dotacao_valor_serializer import DotacaoValorLookUpSerializer

user_model = get_user_model()


class FiscalLoteSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    rf = serializers.SerializerMethodField()

    def get_nome(self, obj):
        return obj.fiscal.nome

    def get_rf(self, obj):
        return obj.fiscal.username

    class Meta:
        model = FiscalLote
        fields = ('nome', 'rf')


class LoteSerializer(serializers.ModelSerializer):
    unidades = serializers.SerializerMethodField()
    nome_fiscal = serializers.SerializerMethodField()
    rf_fiscal = serializers.SerializerMethodField()
    suplentes = serializers.SerializerMethodField()

    def get_unidades(self, obj):
        return UnidadeSerializer(obj.unidades, many=True).data

    def get_nome_fiscal(self, obj):
        if obj.fiscais_lote.filter(tipo_fiscal=FiscalLote.FISCAL_TITULAR).exists():
            fiscal_titular = obj.fiscais_lote.get(tipo_fiscal=FiscalLote.FISCAL_TITULAR)
            return fiscal_titular.fiscal.nome
        return None

    def get_rf_fiscal(self, obj):
        if obj.fiscais_lote.filter(tipo_fiscal=FiscalLote.FISCAL_TITULAR).exists():
            fiscal_titular = obj.fiscais_lote.get(tipo_fiscal=FiscalLote.FISCAL_TITULAR)
            return fiscal_titular.fiscal.username
        return None

    def get_suplentes(self, obj):
        return FiscalLoteSerializer(obj.fiscais_lote.filter(tipo_fiscal=FiscalLote.FISCAL_SUPLENTE), many=True).data

    class Meta:
        model = Lote
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    CONT = 0
    data_encerramento = serializers.SerializerMethodField('get_data_encerramento')
    tipo_servico = TipoServicoLookupSerializer()
    empresa_contratada = EmpresaLookUpSerializer()
    nucleo_responsavel = NucleoLookUpSerializer()
    gestor = UsuarioLookUpSerializer()
    coordenador = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=user_model.objects.all()
    )
    suplente = UsuarioLookUpSerializer()
    edital = EditalListaSerializer()
    total_mensal = serializers.SerializerMethodField('get_total_mensal')
    row_index = serializers.SerializerMethodField('get_row_index')
    dias_para_o_encerramento = serializers.SerializerMethodField('get_dias_para_o_encerramento')
    dres = serializers.SerializerMethodField('get_dres')
    lotes = LoteSerializer(many=True)
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
        queryset=Edital.objects.all()
    )
    unidades_selecionadas = serializers.ListField(required=False)
    lotes = LoteSerializer(many=True, required=False)
    dotacoes = DotacaoValorLookUpSerializer(many=True, required=False)
    dotacoes_orcamentarias = serializers.ListField(required=False)
    dias_para_o_encerramento = serializers.CharField(required=False)

    def validate(self, attrs):
        gestor_e_suplente_devem_ser_diferentes(attrs.get('gestor'), attrs.get('suplente'))
        return attrs

    def update(self, instance, validated_data):
        unidades_selecionadas = validated_data.pop('unidades_selecionadas', [])
        dotacoes = validated_data.pop('dotacoes_orcamentarias', [])
        instance.lotes.all().delete()
        instance.dotacoes.all().delete()
        update_instance_from_dict(instance, validated_data, save=True)

        for dotacao in dotacoes:
            dotacao_valor = DotacaoValor(
                contrato=instance,
                dotacao_orcamentaria=dotacao.get('dotacao_orcamentaria', ''),
                valor=dotacao.get('valor', '')
            )
            dotacao_valor.save()

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
                unidade.logradouro = unidade_json.get('logradouro', '')
                unidade.bairro = unidade_json.get('bairro', '')
                unidade.dre = unidade_json.get('nm_exibicao_diretoria_referencia', '')
                unidade.tipo_unidade = unidade_json.get('sg_tp_escola', '') or ''
                unidade.save()
            else:
                unidade = Unidade(
                    equipamento=Unidade.get_equipamento_from_unidade(unidade_json),
                    tipo_unidade=unidade_json.get('sg_tp_escola', '') or '',
                    codigo_eol=unidade_json.get('cd_equipamento', ''),
                    nome=unidade_json.get('nm_equipamento', ''),
                    logradouro=unidade_json.get('logradouro', ''),
                    bairro=unidade_json.get('bairro', ''),
                    dre=unidade_json.get('nm_exibicao_diretoria_referencia', '')
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


class ContratoSimplesSerializer(serializers.ModelSerializer):
    nome_empresa = serializers.SerializerMethodField()
    data_encerramento = serializers.SerializerMethodField()
    objeto = serializers.SerializerMethodField()

    def get_nome_empresa(self, obj):
        return obj.empresa_contratada.nome

    def get_data_encerramento(self, obj):
        return obj.data_encerramento.strftime('%d/%m/%Y')

    def get_objeto(self, obj):
        return obj.tipo_servico.nome

    class Meta:
        model = Contrato
        fields = ('uuid', 'nome_empresa', 'termo_contrato', 'situacao', 'objeto', 'data_encerramento')
