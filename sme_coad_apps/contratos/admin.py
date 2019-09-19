from django.contrib import admin

from .models import TipoServico, Empresa


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
