from django.contrib import admin

from sme_coad_apps.divisoes.models import Divisao, Nucleo


@admin.register(Divisao)
class DivisaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'ativo')
    ordering = ('nome', 'sigla', 'ativo')


@admin.register(Nucleo)
class NucleoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'ativo')
    ordering = ('nome', 'sigla', 'ativo')
