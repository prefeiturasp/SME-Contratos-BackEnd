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


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'termo_contrato',
        'processo',
        'tipo_servico',
        'empresa_contratada',
        'data_ordem_inicio',
        'data_encerramento',
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
