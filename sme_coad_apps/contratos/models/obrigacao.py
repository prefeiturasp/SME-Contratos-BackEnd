from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .edital import Edital


class GrupoObrigacao(ModeloBase):
    historico = AuditlogHistoryField()
    nome = models.CharField('Nome do Grupo', max_length=100)
    edital = models.ForeignKey(Edital, on_delete=models.CASCADE, related_name='grupos_de_obrigacao')

    def __str__(self):
        return f'{self.edital.numero} - {self.nome}'

    class Meta:
        verbose_name = 'Grupo de Obrigação'
        verbose_name_plural = 'Grupos de Obrigações'


class Obrigacao(ModeloBase):
    historico = AuditlogHistoryField()
    descricao = models.TextField('Descrição')
    item = models.CharField(max_length=15)
    grupo = models.ForeignKey(GrupoObrigacao, on_delete=models.CASCADE, related_name='itens_de_obrigacao')

    def __str__(self):
        return f'{self.item} - {self.descricao}'

    class Meta:
        verbose_name = 'Obrigação'
        verbose_name_plural = 'Obrigações'


auditlog.register(GrupoObrigacao)
auditlog.register(Obrigacao)
