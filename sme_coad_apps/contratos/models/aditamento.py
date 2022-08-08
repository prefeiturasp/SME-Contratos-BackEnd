from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from multiselectfield import MultiSelectField

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class Aditamento(ModeloBase):
    # Objeto Choice
    OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL = 'PRORROGACAO_VIGENCIA_CONTRATUAL'
    OBJETO_MODIFICACAO_PROJETO_ESPECIFICACOES = 'MODIFICACAO_PROJETO_ESPECIFICACOES'
    OBJETO_MODIFICACAO_VALOR_CONTRATUAL = 'MODIFICACAO_VALOR_CONTRATUAL'
    OBJETO_SUBSTITUICAO_GARANTIA_EXECUCAO = 'SUBSTITUICAO_GARANTIA_EXECUCAO'
    OBJETO_MODIFICACAO_REGIME_EXECUCAO = 'MODIFICACAO_REGIME_EXECUCAO'
    OBJETO_MODIFICACAO_FORMA_PAGAMENTO = 'MODIFICACAO_FORMA_PAGAMENTO'

    OBJETOS_NOMES = {
        OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL: 'Prorrogação da vigência contratual',
        OBJETO_MODIFICACAO_PROJETO_ESPECIFICACOES: 'Modificação do projeto ou das especificações, para melhor '
                                                   'adequação técnica os seus objetivos',
        OBJETO_MODIFICACAO_VALOR_CONTRATUAL: 'Modificação do valor contratual em decorrência de acréscimo ou '
                                             'diminuição quantitativa de seu objeto',
        OBJETO_SUBSTITUICAO_GARANTIA_EXECUCAO: 'Substituição da garantia de execução',
        OBJETO_MODIFICACAO_REGIME_EXECUCAO: 'Modificação do regime de execução da obra ou serviço e do modo'
                                            ' de fornecimento',
        OBJETO_MODIFICACAO_FORMA_PAGAMENTO: 'Modificação da forma de pagamento, por imposição de circunstâncias '
                                            'supervenientes, mantido o valor inicial atualizado',
    }

    OBJETO_CHOICES = (
        (OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL, OBJETOS_NOMES[OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL]),
        (OBJETO_MODIFICACAO_PROJETO_ESPECIFICACOES, OBJETOS_NOMES[OBJETO_MODIFICACAO_PROJETO_ESPECIFICACOES]),
        (OBJETO_MODIFICACAO_VALOR_CONTRATUAL, OBJETOS_NOMES[OBJETO_MODIFICACAO_VALOR_CONTRATUAL]),
        (OBJETO_SUBSTITUICAO_GARANTIA_EXECUCAO, OBJETOS_NOMES[OBJETO_SUBSTITUICAO_GARANTIA_EXECUCAO]),
        (OBJETO_MODIFICACAO_REGIME_EXECUCAO, OBJETOS_NOMES[OBJETO_MODIFICACAO_REGIME_EXECUCAO]),
        (OBJETO_MODIFICACAO_FORMA_PAGAMENTO, OBJETOS_NOMES[OBJETO_MODIFICACAO_FORMA_PAGAMENTO]),
    )
    historico = AuditlogHistoryField()
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='aditamentos')
    termo_aditivo = models.CharField('TA No.', max_length=10, unique=True)
    objeto_aditamento = MultiSelectField(choices=OBJETO_CHOICES)
    data_inicial = models.DateField('Data Inicial', null=True)
    data_final = models.DateField('Data Final', null=True)
    valor_mensal_atualizado = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True)
    valor_total_atualizado = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True)
    valor_aditamento = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True)
    razoes_aditamento = models.TextField('Razões do aditamento')

    def __str__(self):
        return self.termo_aditivo

    @classmethod
    def objetos_to_json(cls):
        result = []
        for objeto in cls.OBJETO_CHOICES:
            choice = {
                'id': objeto[0],
                'nome': objeto[1]
            }
            result.append(choice)
        return result

    class Meta:
        verbose_name = 'Aditamento'
        verbose_name_plural = 'Aditamentos'


auditlog.register(Aditamento)
