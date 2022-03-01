from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from sme_coad_apps.users.models import User

from ..models_abstracts import SingletonModel


class Coad(SingletonModel):
    historico = AuditlogHistoryField()
    coordenador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='coordenador_coad', blank=True,
                                    null=True)

    def __str__(self):
        return 'COAD (Registro Único)'

    class Meta:
        verbose_name = 'COAD'
        verbose_name_plural = 'COAD'


auditlog.register(Coad)
