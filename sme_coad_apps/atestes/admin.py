from django.contrib import admin
from .models import ModeloAteste, GrupoVerificacao, ItensVerificacao


class GrupoVerificacaoInline(admin.StackedInline):
    extra = 1
    model = GrupoVerificacao


class ItensVerificacaoInline(admin.StackedInline):
    extra = 1
    model = ItensVerificacao
    readonly_fields = ['item']
    fieldsets = (
        (None, {
            'fields': ('item', 'descricao')
        }),
    )


@admin.register(ModeloAteste)
class ModeloAtesteAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    ordering = ('titulo',)
    search_fields = ('titulo',)
    inlines = [
        GrupoVerificacaoInline
    ]


@admin.register(GrupoVerificacao)
class GrupoVerificacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)
    inlines = [
        ItensVerificacaoInline
    ]
