from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from ...core.models_abstracts import ModeloBase


class Edital(ModeloBase):
    historico = AuditlogHistoryField()
    numero = models.CharField('Número do Edital', max_length=100)

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'Edital'
        verbose_name_plural = 'Editais'


auditlog.register(Edital)
