from django.contrib import admin
from django.utils.html import format_html

from .models import RequisicaoApiSofi


@admin.register(RequisicaoApiSofi)
class RequisicacaoSofiAdmin(admin.ModelAdmin):
    def get_status(self, obj):
        color = 'green'
        if obj.status == 'ERRO':
            color = 'red'
        return format_html(
            f'<div style="width:80px; color:white; text-align:center; background:{color}; '
            f'border-radius:5px;">{obj.get_status_display()}</div>'
        )

    def get_data(self, obj):
        return obj.data.strftime('%d/%m/%Y')

    def get_hora(self, obj):
        return obj.data.strftime('%H:%M')

    get_status.short_description = 'Status'
    get_data.short_description = 'Data'
    get_hora.short_description = 'Hora'

    list_display = ('endpoint', 'get_data', 'get_hora', 'get_status')
    list_filter = ('endpoint', 'status')
    search_fields = ('endpoint',)
