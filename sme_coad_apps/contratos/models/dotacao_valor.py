from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class DotacaoOrcamentaria(ModeloBase):
    historico = AuditlogHistoryField()
    orgao = models.CharField('Órgão', max_length=2)
    unidade = models.CharField('Unidade', max_length=2)
    funcao = models.CharField('Função', max_length=2)
    subfuncao = models.CharField('Subfunção', max_length=3)
    programa = models.CharField('Programa', max_length=4)
    projeto_atividade = models.CharField('Projeto/Atividade', max_length=5)
    conta_despesa = models.CharField('Conta Despesa', max_length=8)
    fonte = models.CharField('Fonte', max_length=2)

    @property
    def numero_dotacao(self):
        return (f'{self.orgao}.{self.unidade}.{self.funcao}.{self.subfuncao}.'
                f'{self.programa}.{self.projeto_atividade}.{self.conta_despesa}.{self.fonte}')

    def __str__(self):
        return self.numero_dotacao

    class Meta:
        verbose_name = 'Dotação Orçamentária'
        verbose_name_plural = 'Dotações Orçamentárias'


class DotacaoValor(ModeloBase):
    historico = AuditlogHistoryField()
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='dotacoes')
    dotacao_orcamentaria = models.ForeignKey(DotacaoOrcamentaria, on_delete=models.PROTECT,
                                             related_name='dotacoes_por_valor')
    valor = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.contrato.termo_contrato} - {self.dotacao_orcamentaria} - R${self.valor}'

    class Meta:
        verbose_name = 'Dotação Orçamentária (Valor)'
        verbose_name_plural = 'Dotações Orçamentárias (Valor)'


class Empenho(ModeloBase):
    historico = AuditlogHistoryField()
    dotacao_valor = models.ForeignKey(DotacaoValor, on_delete=models.CASCADE, related_name='empenhos')
    numero = models.CharField('Número do Empenho', max_length=20)
    valor_previsto = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Empanheo Nº: {self.numero} - R${self.valor_previsto}'

    class Meta:
        verbose_name = 'Empenho'
        verbose_name_plural = 'Empenhos'


auditlog.register(DotacaoOrcamentaria)
auditlog.register(DotacaoValor)
auditlog.register(Empenho)
