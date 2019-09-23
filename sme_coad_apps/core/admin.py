from django.contrib import admin

from .models import Divisao, Nucleo, Unidade


@admin.register(Divisao)
class DivisaoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    ordering = ('sigla', 'nome')
    search_fields = ('sigla', 'nome')


@admin.register(Nucleo)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('divisao', 'sigla', 'nome')
    ordering = ('divisao__nome', 'sigla', 'nome')
    search_fields = ('sigla', 'nome')


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('equipamento', 'nome', 'tipo_unidade', 'codigo_eol')
    ordering = ('equipamento', 'nome', 'tipo_unidade', 'codigo_eol')
    search_fields = ('nome', 'codigo_eol')
    list_filter = ('equipamento', 'tipo_unidade')
