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


class ContratoUnidadeInLine(admin.TabularInline):
    model = ContratoUnidade
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = (
        'processo',
        'tipo_servico',
        'termo_contrato',
        'empresa_contratada',
        'data_ordem_inicio',
        'data_encerramento',
        'situacao'
    )
    ordering = ('processo', 'tipo_servico', 'termo_contrato', 'empresa_contratada')
    search_fields = ('processo', 'termo_contrato')
    list_filter = ('tipo_servico', 'empresa_contratada', 'situacao')
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
                ('data_assinatura', 'data_ordem_inicio', 'vigencia_em_meses'),
                'observacoes',
                'gestor',
                'situacao',
            )
        }
         ),
    )
