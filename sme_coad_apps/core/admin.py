from django.contrib import admin

from .models import Divisao, Nucleo


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
