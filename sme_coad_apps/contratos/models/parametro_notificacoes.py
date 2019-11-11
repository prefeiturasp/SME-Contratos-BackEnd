from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from .contrato import Contrato
from ...core.models_abstracts import ModeloBase


class ParametroNotificacoesVigencia(ModeloBase):
    historico = AuditlogHistoryField()

    estado_contrato = models.CharField('Para contratos com estado', max_length=15, choices=Contrato.ESTADO_CHOICES,
                                       blank=True, default='')
    vencendo_em = models.PositiveSmallIntegerField('Vencendo a partir de (dias)', default=0, blank=True, null=True)
    repetir_notificacao_a_cada = models.PositiveSmallIntegerField('Repetir notificação a cada (dias)', default=0,
                                                                  blank=True, null=True)

    def __str__(self):
        return f"Contratos {Contrato.ESTADO_NOMES[self.estado_contrato]} " \
               f"notificar a partir de {self.vencendo_em} dias " \
               f"repetindo a cada {self.repetir_notificacao_a_cada} dias."

    class Meta:
        verbose_name = "Parâmetro de notificação de vigência"
        verbose_name_plural = "Parâmetros de notificação de vigência"

        unique_together = [['estado_contrato', 'vencendo_em']]


auditlog.register(ParametroNotificacoesVigencia)
