from django.db import models

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from sme_coad_apps.users.models import User
from ..models_abstracts import SingletonModel, ModeloBase


class Coad(SingletonModel):
    historico = AuditlogHistoryField()
    coordenador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='coordenador_coad', blank=True,
                                    null=True)

    def __str__(self):
        return "COAD (Registro Único)"

    class Meta:
        verbose_name = "COAD"
        verbose_name_plural = "COAD"


class CoadAssessor(ModeloBase):
    historico = AuditlogHistoryField()
    coad = models.ForeignKey(Coad, on_delete=models.CASCADE, related_name='assessores')
    assessor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assessor_coad')

    def __str__(self):
        return f"{self.assessor.nome}"

    class Meta:
        verbose_name = "Assessor COAD"
        verbose_name_plural = "Assessores COAD"


auditlog.register(Coad)
auditlog.register(CoadAssessor)
