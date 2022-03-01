from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class ObrigacaoContratual(ModeloBase):
    historico = AuditlogHistoryField()
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='obrigacoes_contratuais')
    item = models.CharField(max_length=15)
    obrigacao = models.TextField(default='')

    def __str__(self):
        return f'{self.contrato.termo_contrato} - {self.obrigacao}'

    class Meta:
        verbose_name = 'Obrigação Contratual'
        verbose_name_plural = 'Obrigações Contratuais'


auditlog.register(ObrigacaoContratual)
