from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase


class TipoServico(ModeloBase):
    historico = AuditlogHistoryField()

    nome = models.CharField('Nome', max_length=160, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Serviço'
        verbose_name_plural = 'Tipos de Serviço'


auditlog.register(TipoServico)
