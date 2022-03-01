from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from sme_coad_apps.users.models import User

from ..models_abstracts import ModeloBase
from .coad import Coad


class CoadAssessor(ModeloBase):
    historico = AuditlogHistoryField()
    coad = models.ForeignKey(Coad, on_delete=models.CASCADE, related_name='assessores')
    assessor = models.OneToOneField(User, on_delete=models.PROTECT, related_name='assessor_coad')

    def __str__(self):
        return f'{self.assessor.nome}'

    @classmethod
    def limpa_assessores(cls):
        cls.objects.all().delete()

    @classmethod
    def append_assessores(cls, assessores):
        coad = Coad.objects.get(id=1)
        for assessor in assessores:
            usuario = User.objects.get(username=assessor['assessor']['username'])
            cls.objects.create(coad=coad, assessor=usuario)

    class Meta:
        verbose_name = 'Assessor COAD'
        verbose_name_plural = 'Assessores COAD'


auditlog.register(CoadAssessor)
