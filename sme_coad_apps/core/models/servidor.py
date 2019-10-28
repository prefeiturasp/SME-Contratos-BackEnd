from django.db import models

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from sme_coad_apps.users.models import User
from ..models_abstracts import ModeloBase
from .nucleo import Nucleo


class Servidor(ModeloBase):
    historico = AuditlogHistoryField()
    nucleo = models.ForeignKey(Nucleo, on_delete=models.CASCADE, related_name='servidores')
    servidor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='servidor')

    def __str__(self):
        return f"{self.servidor.nome}"

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"


auditlog.register(Servidor)

