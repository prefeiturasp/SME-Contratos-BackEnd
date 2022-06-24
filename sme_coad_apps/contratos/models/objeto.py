from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase


class Objeto(ModeloBase):
    historico = AuditlogHistoryField()

    nome = models.CharField('Nome', max_length=160, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Objeto'
        verbose_name_plural = 'Objetos'


auditlog.register(Objeto)
