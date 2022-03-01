import datetime

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class ParametroNotificacoesVigencia(ModeloBase):
    historico = AuditlogHistoryField()

    estado_contrato = models.CharField('Para contratos com estado', max_length=30, choices=Contrato.ESTADO_CHOICES,
                                       blank=True, default='')
    vencendo_em = models.PositiveSmallIntegerField('Vencendo a partir de (dias)', default=0, blank=True, null=True)
    repetir_notificacao_a_cada = models.PositiveSmallIntegerField('Repetir notificação a cada (dias)', default=0,
                                                                  blank=True, null=True)

    def __str__(self):
        contratos_no_estado = f'Contratos {Contrato.ESTADO_NOMES[self.estado_contrato]}'
        notificar_a_partir_de = f'notificar a partir de {self.vencendo_em} dias'
        repetir_a_cada = f'repetindo a cada {self.repetir_notificacao_a_cada} dias'
        return f'{contratos_no_estado} {notificar_a_partir_de} {repetir_a_cada}.'

    @classmethod
    def parametros_do_estado(cls, estado, crescente=False):
        ordem = 'vencendo_em' if crescente else '-vencendo_em'
        return cls.objects.filter(estado_contrato=estado).order_by(ordem)

    @classmethod
    def data_limite_do_estado(cls, estado):
        maior_limite = cls.parametros_do_estado(estado).first().vencendo_em
        data_limite = datetime.date.today() + datetime.timedelta(days=maior_limite)
        return data_limite

    @classmethod
    def estado_notificavel(cls, estado):
        return cls.objects.filter(estado_contrato=estado).count() > 0

    @classmethod
    def frequencia_repeticao(cls, estado, dias_pra_vencer):
        parametros_estado = cls.parametros_do_estado(estado, crescente=True)
        frequencia = 0
        for parametro in parametros_estado:
            if parametro.vencendo_em > dias_pra_vencer:
                frequencia = parametro.repetir_notificacao_a_cada
                break
        return frequencia

    class Meta:
        verbose_name = 'Parâmetro de notificação de vigência'
        verbose_name_plural = 'Parâmetros de notificação de vigência'

        unique_together = [['estado_contrato', 'vencendo_em']]


auditlog.register(ParametroNotificacoesVigencia)
