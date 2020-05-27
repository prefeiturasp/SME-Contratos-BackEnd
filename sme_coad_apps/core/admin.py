from django.contrib import admin

from .models import Divisao, Nucleo, Unidade, Coad, CoadAssessor, Servidor, Edital, GrupoObrigacao, Obrigacao


class NucleoInLine(admin.TabularInline):
    model = Nucleo
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Divisao)
class DivisaoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    ordering = ('sigla',)
    search_fields = ('sigla', 'nome')
    inlines = [NucleoInLine]


class ServidoresInLine(admin.TabularInline):
    model = Servidor
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Nucleo)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'divisao')
    ordering = ('divisao__sigla', 'sigla')
    search_fields = ('sigla', 'nome')
    list_display_links = ('sigla', 'nome')

    inlines = [ServidoresInLine]


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipamento', 'tipo_unidade', 'codigo_eol', 'sigla', 'dre')
    ordering = ('nome',)
    search_fields = ('nome', 'codigo_eol', 'sigla')
    list_filter = ('equipamento', 'tipo_unidade', 'dre')
    list_display_links = ('nome',)


class CoadAssessorInLine(admin.TabularInline):
    model = CoadAssessor
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Coad)
class CoadAdmin(admin.ModelAdmin):
    inlines = [CoadAssessorInLine]


@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    ...


class GrupoObrigacoesInline(admin.StackedInline):
    extra = 1
    model = GrupoObrigacao


class ObrigacaoInline(admin.StackedInline):
    extra = 1
    model = Obrigacao
    fieldsets = (
        (None, {
            'fields': ('item', 'descricao')
        }),
    )


@admin.register(Edital)
class EditalAdmin(admin.ModelAdmin):
    list_display = ('numero',)
    ordering = ('numero',)
    search_fields = ('numero',)
    inlines = [
        GrupoObrigacoesInline
    ]


@admin.register(GrupoObrigacao)
class GrupoObrigacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)
    inlines = [
        ObrigacaoInline
    ]
