from django.contrib.auth import get_user_model
from rest_framework import serializers

from ....core.api.serializers.nucleo_serializer import NucleoLookUpSerializer
from ....core.api.serializers.unidade_serializer import UnidadeSerializer
from ....core.helpers.update_instance_from_dict import update_instance_from_dict
from ....core.models import Nucleo, Unidade
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer
from ....users.models import User
from ...api.serializers.edital_serializer import EditalSimplesSerializer
from ...api.serializers.empresa_serializer import EmpresaSerializer
from ...api.serializers.objeto_serializer import ObjetoLookupSerializer
from ...models import Ata, Contrato, Empresa, FiscalLote, Lote
from ...models.contrato import GestorContrato
from ...models.edital import Edital
from ...models.objeto import Objeto
from ..validations.contrato_validations import nao_pode_repetir_o_gestor
from .ata_serializer import AtaLookUpSerializer
from .contrato_unidade_serializer import ContratoUnidadeSerializer
from .dotacao_valor_serializer import DotacaoValorCreatorSerializer, DotacaoValorSerializer

user_model = get_user_model()


class GestorContratoSerializer(serializers.ModelSerializer):
    gestor = UsuarioLookUpSerializer(required=False)

    class Meta:
        model = GestorContrato
        fields = ('uuid', 'gestor')


class GestorContratoCreatorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Contrato.objects.all()
    )
    gestor = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = GestorContrato
        fields = ('uuid', 'gestor', 'contrato')


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
    objeto = ObjetoLookupSerializer()
    empresa_contratada = EmpresaSerializer()
    nucleo_responsavel = NucleoLookUpSerializer()
    gestores = GestorContratoSerializer(many=True)
    edital = EditalSimplesSerializer()
    ata = AtaLookUpSerializer()
    total_mensal = serializers.SerializerMethodField('get_total_mensal')
    row_index = serializers.SerializerMethodField('get_row_index')
    dias_para_o_encerramento = serializers.SerializerMethodField('get_dias_para_o_encerramento')
    dres = serializers.SerializerMethodField('get_dres')
    lotes = LoteSerializer(many=True)
    dotacoes = DotacaoValorSerializer(many=True)
    unidades = ContratoUnidadeSerializer(many=True)

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
    objeto = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Objeto.objects.all()
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
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Edital.objects.all()
    )
    ata = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Ata.objects.all()
    )
    unidades_selecionadas = serializers.ListField(required=False)
    lotes = LoteSerializer(many=True, required=False)
    dotacoes = DotacaoValorCreatorSerializer(many=True, required=False)
    dias_para_o_encerramento = serializers.CharField(required=False)
    gestores = GestorContratoCreatorSerializer(many=True, required=False)

    def validate(self, attrs):
        nao_pode_repetir_o_gestor(attrs.get('gestores'))
        return attrs

    def create(self, validated_data):
        unidades_selecionadas = validated_data.pop('unidades_selecionadas', [])
        dotacoes = validated_data.pop('dotacoes', [])
        gestores = validated_data.pop('gestores', [])
        contrato = Contrato.objects.create(**validated_data)

        for dotacao in dotacoes:
            dotacao['contrato'] = contrato
            DotacaoValorCreatorSerializer().create(dotacao)

        for gestor in gestores:
            gestor['contrato'] = contrato
            GestorContratoCreatorSerializer().create(gestor)

        for unidade_selecionada in unidades_selecionadas:
            lote = unidade_selecionada.get('lote')
            if contrato.lotes.filter(nome=lote, contrato=contrato).exists():
                lote = contrato.lotes.get(nome=lote, contrato=contrato)
            else:
                lote = Lote(nome=lote, contrato=contrato)
                lote.save()

            unidade_json = unidade_selecionada.get('unidade')
            if Unidade.objects.filter(codigo_eol=unidade_json.get('cd_equipamento')).exists():
                unidade = Unidade.objects.get(codigo_eol=unidade_json.get('cd_equipamento'))
                unidade.logradouro = unidade_json.get('logradouro', '')
                unidade.bairro = unidade_json.get('bairro', '')
                unidade.dre = unidade_json.get('nm_exibicao_diretoria_referencia', '')
                unidade.tipo_unidade = unidade_json.get('sg_tp_escola', '') or ''
                unidade.subprefeitura = unidade_json.get('nomeSubprefeitura', '')
                unidade.save()
            else:
                unidade = Unidade(
                    equipamento=Unidade.get_equipamento_from_unidade(unidade_json),
                    tipo_unidade=unidade_json.get('sg_tp_escola', '') or '',
                    codigo_eol=unidade_json.get('cd_equipamento', ''),
                    nome=unidade_json.get('nm_equipamento', ''),
                    logradouro=unidade_json.get('logradouro', ''),
                    bairro=unidade_json.get('bairro', ''),
                    dre=unidade_json.get('nm_exibicao_diretoria_referencia', ''),
                    subprefeitura=unidade_json.get('nomeSubprefeitura', '')
                )
                unidade.save()
            lote.unidades.add(unidade)

        return contrato

    def update(self, instance, validated_data):
        unidades_selecionadas = validated_data.pop('unidades_selecionadas', [])
        dotacoes = validated_data.pop('dotacoes', [])
        gestores = validated_data.pop('gestores', [])
        lista_gestores_existentes = list(instance.gestores.all().values_list('uuid', flat=True))
        instance.lotes.all().delete()
        instance.dotacoes.all().delete()

        for dotacao in dotacoes:
            dotacao['contrato'] = instance
            DotacaoValorCreatorSerializer().create(dotacao)

        for gestor in gestores:
            manager = gestor.get('uuid', None)
            if manager in lista_gestores_existentes:
                lista_gestores_existentes.remove(manager)
            else:
                gestor['contrato'] = instance
                GestorContratoCreatorSerializer().create(gestor)

        instance.gestores.filter(uuid__in=lista_gestores_existentes).delete()
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
                unidade.logradouro = unidade_json.get('logradouro', '')
                unidade.bairro = unidade_json.get('bairro', '')
                unidade.dre = unidade_json.get('nm_exibicao_diretoria_referencia', '')
                unidade.tipo_unidade = unidade_json.get('sg_tp_escola', '') or ''
                unidade.subprefeitura = unidade_json.get('nomeSubprefeitura', '')
                unidade.save()
            else:
                unidade = Unidade(
                    equipamento=Unidade.get_equipamento_from_unidade(unidade_json),
                    tipo_unidade=unidade_json.get('sg_tp_escola', '') or '',
                    codigo_eol=unidade_json.get('cd_equipamento', ''),
                    nome=unidade_json.get('nm_equipamento', ''),
                    logradouro=unidade_json.get('logradouro', ''),
                    bairro=unidade_json.get('bairro', ''),
                    dre=unidade_json.get('nm_exibicao_diretoria_referencia', ''),
                    subprefeitura=unidade_json.get('nomeSubprefeitura', '')
                )
                unidade.save()
            lote.unidades.add(unidade)
        return instance

    class Meta:
        model = Contrato
        exclude = ('id',)


class ContratoLookUpSerializer(serializers.ModelSerializer):
    gestores = GestorContratoSerializer(many=True)

    class Meta:
        model = Contrato
        fields = ('uuid', 'termo_contrato', 'gestores', 'alterado_em')


class ContratoSimplesSerializer(serializers.ModelSerializer):
    nome_empresa = serializers.SerializerMethodField()
    data_encerramento = serializers.SerializerMethodField()
    objeto = serializers.SerializerMethodField()

    def get_nome_empresa(self, obj):
        return obj.empresa_contratada.nome if obj.empresa_contratada else None

    def get_data_encerramento(self, obj):
        return obj.data_encerramento.strftime('%d/%m/%Y') if obj.data_encerramento else None

    def get_objeto(self, obj):
        return obj.objeto.nome if obj.objeto else None

    class Meta:
        model = Contrato
        fields = ('uuid', 'nome_empresa', 'termo_contrato', 'situacao', 'objeto', 'data_encerramento')
