from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ..models import Divisao
from ..models_abstracts import TemNome, ModeloBase


class Nucleo(ModeloBase, TemNome):
    historico = AuditlogHistoryField()

    sigla = models.CharField('Sigla', max_length=20)
    divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.divisao.sigla}/{self.sigla}-{self.nome}'

    class Meta:
        verbose_name = 'Núcleo'
        verbose_name_plural = 'Núcleos'


auditlog.register(Nucleo)
