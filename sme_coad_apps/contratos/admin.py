from django.contrib import admin
from django.utils import timezone

from sme_coad_apps.contratos.models.contrato import DocumentoFiscal
from .models import NotificacaoVigenciaContrato, ObrigacaoContratual
from .models import (TipoServico, Empresa, Contrato, ContratoUnidade, ColunasContrato, ParametroNotificacoesVigencia,
                     FiscaisUnidade, Lote, FiscalLote, DotacaoValor)


@admin.register(TipoServico)
class TipoServicoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    def get_cnpj_formatado(self, empresa):
        return empresa.cnpj_formatado

    get_cnpj_formatado.short_description = "CNPJ"

    list_display = ('nome', 'get_cnpj_formatado')
    ordering = ('nome',)
    search_fields = ('nome', 'cnpj')


# class ContratoUnidadeInLine(admin.StackedInline):
class ContratoUnidadeInLine(admin.TabularInline):
    model = ContratoUnidade
    raw_id_fields = ("unidade",)
    extra = 1  # Quantidade de linhas que serão exibidas.

    def get_queryset(self, request):
        return super(ContratoUnidadeInLine, self).get_queryset(request).select_related('unidade')


class LotesInLine(admin.TabularInline):
    model = Lote
    filter_horizontal = ('unidades',)
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):

    def dias_para_vencer(self, contrato):
        return contrato.dias_para_o_encerramento

    dias_para_vencer.short_description = 'Dias para vencer'

    def valor_mensal(self, contrato):
        return f"R$ {contrato.total_mensal: 20,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    valor_mensal.short_description = 'Valor Mensal'

    def data_inicio(self, contrato):
        return f'{contrato.data_ordem_inicio:%d/%m/%Y}' if contrato.data_ordem_inicio else ''

    data_inicio.short_description = 'Início'

    def data_fim(self, contrato):
        return f'{contrato.data_encerramento:%d/%m/%Y}' if contrato.data_encerramento else ''

    data_fim.short_description = 'Fim'

    def atualiza_tipo_equipamento(self, request, queryset):
        """
        Foram criados campos no contrato para permitir a consulta por tipo de equipamento
        Esses campos são atualizados automaticamente pelo modelo de Contrato, mas para contratos que já existiam
        esses campos precisam ser atualizados.
        Essa task foi criada para permitir a atualização desses contratos em produção.
        """

        for contrato in queryset.all():
            contrato.save()

        self.message_user(request, "Tipo de equipamento atualizado nos contratos.")

    atualiza_tipo_equipamento.short_description = 'Atualizar tipo de equipamento'

    def encerra_contratos_vencidos(self, request, queryset):
        contratos = queryset.filter(data_encerramento__lt=timezone.now()).exclude(
            situacao=Contrato.SITUACAO_ENCERRADO)

        for contrato in contratos:
            contrato.situacao = Contrato.SITUACAO_ENCERRADO
            contrato.save()
        self.message_user(request, "Contratos vencidos encerrados.")

    encerra_contratos_vencidos.short_description = 'Encerrar contratos vencidos'

    list_display = (
        'termo_contrato',
        'tipo_servico',
        'empresa_contratada',
        'dres',
        'data_inicio',
        'data_fim',
        'dias_para_vencer',
        'estado_contrato',
        'situacao'
    )
    ordering = ('termo_contrato',)
    search_fields = ('processo', 'termo_contrato')
    list_filter = ('tipo_servico', 'empresa_contratada', 'situacao', 'estado_contrato')
    inlines = [ContratoUnidadeInLine, LotesInLine]
    readonly_fields = ('tem_ceu', 'tem_ua', 'tem_ue')
    fieldsets = (
        ('Contrato', {
            'fields': (
                'termo_contrato',
                'processo',
                'edital',
                'tipo_servico',
                'nucleo_responsavel',
                'objeto',
                'empresa_contratada',
                'modelo_ateste',
                ('data_assinatura', 'data_ordem_inicio', 'vigencia_em_dias', 'unidade_vigencia'),
                'referencia_encerramento',
                'observacoes',
                'coordenador',
                'gestor',
                'suplente',
                'situacao',
                'tem_ue',
                'tem_ceu',
                'tem_ua',
            )
        }
         ),
    )

    list_select_related = ('nucleo_responsavel', 'empresa_contratada', 'gestor', 'suplente', 'tipo_servico')

    actions = ['atualiza_tipo_equipamento', 'encerra_contratos_vencidos']


@admin.register(ColunasContrato)
class ColunasContratoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'colunas_array')
    ordering = ('usuario',)
    search_fields = ('usuario',)


@admin.register(DocumentoFiscal)
class DocumentoFiscalAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'tipo_unidade', 'criado_em']
    ordering = ('contrato',)
    search_field = ('contrato', 'tipo_unidade')


@admin.register(ParametroNotificacoesVigencia)
class ParametroNotificacoesVigenciaAdmin(admin.ModelAdmin):
    list_display = ('estado_contrato', 'vencendo_em', 'repetir_notificacao_a_cada')
    ordering = ('estado_contrato',)
    list_filter = ('estado_contrato',)


@admin.register(NotificacaoVigenciaContrato)
class NotificacaoVigenciaContratoAdmin(admin.ModelAdmin):
    def termo_contrato(self, notificacao):
        return notificacao.contrato.termo_contrato

    list_display = ('criado_em', 'termo_contrato', 'notificado')
    ordering = ('criado_em', 'contrato', 'notificado')
    list_filter = ('notificado',)


@admin.register(ObrigacaoContratual)
class ObrigacaoContratualAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'item', 'obrigacao', ]
    ordering = ('contrato',)


class FiscaisContratoUnidadeInLine(admin.TabularInline):
    model = FiscaisUnidade
    extra = 1  # Quantidade de linhas que serão exibidas.


class FiscaisLoteInLine(admin.TabularInline):
    model = FiscalLote
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(ContratoUnidade)
class ContratoUnidadeAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'unidade', 'lote', ]
    ordering = ('contrato',)
    list_filter = ('contrato',)
    inlines = [FiscaisContratoUnidadeInLine]


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    filter_horizontal = ('unidades',)
    inlines = [FiscaisLoteInLine]
    model = Lote


@admin.register(DotacaoValor)
class DotacaoValorAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'dotacao_orcamentaria', 'valor', ]
    ordering = ('contrato',)
