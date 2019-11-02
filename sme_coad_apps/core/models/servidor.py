from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from sme_coad_apps.users.models import User
from .nucleo import Nucleo
from ..models_abstracts import ModeloBase


class Servidor(ModeloBase):
    historico = AuditlogHistoryField()
    nucleo = models.ForeignKey(Nucleo, on_delete=models.CASCADE, related_name='servidores')
    servidor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='servidor')

    def __str__(self):
        return f"{self.servidor.nome}"

    @classmethod
    def append_servidores(cls, nucleo=None, servidores=[]):
        if not nucleo or not servidores:
            return

        for servidor in servidores:
            usuario = User.objects.get(username=servidor["username"])
            cls.objects.create(nucleo=nucleo, servidor=usuario)

    @classmethod
    def limpa_servidores(cls, nucleo=None):
        if not nucleo:
            return

        cls.objects.filter(nucleo=nucleo).delete()

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"


auditlog.register(Servidor)

