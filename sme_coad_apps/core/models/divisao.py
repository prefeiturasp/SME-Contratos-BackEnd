from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from sme_coad_apps.users.models import User

from ..models_abstracts import ModeloBase, TemNome


class Divisao(ModeloBase, TemNome):
    historico = AuditlogHistoryField()

    sigla = models.CharField('Sigla', max_length=15, unique=True)
    diretor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='diretor_divisao', blank=True, null=True)
    suplente_diretor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='suplente_diretor_divisao',
                                         blank=True, null=True)

    def __str__(self):
        return f'{self.sigla}-{self.nome}'

    class Meta:
        verbose_name = 'Divisão'
        verbose_name_plural = 'Divisões'


auditlog.register(Divisao)
