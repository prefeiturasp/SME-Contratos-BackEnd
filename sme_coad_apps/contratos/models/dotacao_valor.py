from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class DotacaoValor(ModeloBase):
    historico = AuditlogHistoryField()
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='dotacoes')
    dotacao_orcamentaria = models.TextField('Dotação Orçamentária', default='')
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.contrato.termo_contrato} - {self.dotacao_orcamentaria} - R${self.valor}'

    class Meta:
        verbose_name = 'Dotação Orçamentária'
        verbose_name_plural = 'Dotações Orçamentárias'


auditlog.register(DotacaoValor)
