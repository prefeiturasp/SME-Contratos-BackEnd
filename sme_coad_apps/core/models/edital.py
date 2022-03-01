from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase


class Edital(ModeloBase):
    historico = AuditlogHistoryField()
    numero = models.CharField('Número do Edital', max_length=50, unique=True)

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'Edital'
        verbose_name_plural = 'Editais'


auditlog.register(Edital)
