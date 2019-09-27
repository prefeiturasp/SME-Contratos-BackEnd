import locale

from django.contrib import admin

from .models import TipoServico, Empresa, Contrato, ContratoUnidade


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


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):

    def dias_para_vencer(self, contrato):
        return contrato.dias_para_o_encerramento

    dias_para_vencer.short_description = 'Dias para vencer'

    def valor_mensal(self, contrato):
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        return locale.currency(contrato.total_mensal, grouping=True)

    valor_mensal.short_description = 'Valor Mensal'

    def data_inicio(self, contrato):
        return f'{contrato.data_ordem_inicio:%d/%m/%Y}'

    data_inicio.short_description = 'Início'

    def data_fim(self, contrato):
        return f'{contrato.data_encerramento:%d/%m/%Y}'

    data_fim.short_description = 'Fim'

    list_display = (
        'termo_contrato',
        'processo',
        'tipo_servico',
        'empresa_contratada',
        'valor_mensal',
        'data_inicio',
        'data_fim',
        'dias_para_vencer',
        'estado_contrato',
        'situacao'
    )
    ordering = ('termo_contrato',)
    search_fields = ('processo', 'termo_contrato')
    list_filter = ('tipo_servico', 'empresa_contratada', 'situacao', 'estado_contrato')
    inlines = [ContratoUnidadeInLine]

    fieldsets = (
        ('Contrato', {
            'fields': (
                'termo_contrato',
                'processo',
                'tipo_servico',
                'nucleo_responsavel',
                'objeto',
                'empresa_contratada',
                ('data_assinatura', 'data_ordem_inicio', 'vigencia_em_dias'),
                'observacoes',
                'gestor',
                'situacao',
            )
        }
         ),
    )

    list_select_related = ('nucleo_responsavel', 'empresa_contratada', 'gestor', 'tipo_servico')
