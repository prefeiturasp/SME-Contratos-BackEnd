from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

from ...core.models_abstracts import ModeloBase
from ...core.models.edital import Edital


class ClausulaObrigacao(ModeloBase):
    historico = AuditlogHistoryField()
    item = models.CharField(max_length=15)
    nome = models.CharField('Nome da Cláusula', max_length=350)
    edital = models.ForeignKey(Edital, on_delete=models.CASCADE, related_name="clausulas_de_obrigacao")

    def __str__(self):
        return f'{self.edital.numero} - {self.item} {self.nome}'

    class Meta:
        verbose_name = 'Cláusula de Obrigação'
        verbose_name_plural = 'Cláusulas de Obrigações'


class GrupoObrigacao(ModeloBase):
    historico = AuditlogHistoryField()
    item = models.CharField(max_length=15)
    nome = models.CharField('Nome do Grupo', max_length=350)
    clausula = models.ForeignKey(ClausulaObrigacao, on_delete=models.CASCADE, related_name="grupos_de_obrigacao")

    def __str__(self):
        return f'{self.item} - {self.nome}'

    class Meta:
        verbose_name = 'Grupo de Obrigação'
        verbose_name_plural = 'Grupos de Obrigações'


class ItemObrigacao(ModeloBase):
    historico = AuditlogHistoryField()
    descricao = models.TextField('Descrição do Item')
    item = models.CharField(max_length=15)
    grupo = models.ForeignKey(GrupoObrigacao, on_delete=models.CASCADE, related_name="itens_de_obrigacao")

    def __str__(self):
        return f'{self.item} - {self.descricao}'

    class Meta:
        verbose_name = 'Item de Obrigação'
        verbose_name_plural = 'Itens de Obrigações'


class SubItemObrigacao(ModeloBase):
    historico = AuditlogHistoryField()
    descricao = models.TextField('Descrição do Sub Item')
    item = models.CharField(max_length=15)
    item_obrigacao = models.ForeignKey(ItemObrigacao, on_delete=models.CASCADE, related_name="sub_itens_de_obrigacao")

    def __str__(self):
        return f'{self.item} - {self.descricao}'

    class Meta:
        verbose_name = 'Sub Item de Obrigação'
        verbose_name_plural = 'Sub Itens de Obrigações'


auditlog.register(ClausulaObrigacao)
auditlog.register(GrupoObrigacao)
auditlog.register(ItemObrigacao)
auditlog.register(SubItemObrigacao)
