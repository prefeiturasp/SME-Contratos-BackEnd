from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from ..models.tipo_servico import TipoServico


class Edital(ModeloBase):

    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'

    STATUS_CHOICES = (
        (ATIVO, 'Ativo'),
        (INATIVO, 'Inativo'),
    )

    # Tipos de contratação choice
    TIPO_LICITACAO = 'LICITACAO'
    TIPO_DISPENSA_LICITACAO = 'DISPENSA_LICITACAO'
    TIPO_INEXIGIBILIDADE_LICITACAO = 'INEXIGIBILIDADE_LICITACAO'

    TIPO_NOMES = {
        TIPO_LICITACAO: 'Licitação',
        TIPO_DISPENSA_LICITACAO: 'Dispensa de Licitação',
        TIPO_INEXIGIBILIDADE_LICITACAO: 'Inexigibilidade de Licitação"',
    }

    TIPO_CONTRATACAO_CHOICES = (
        (TIPO_LICITACAO, TIPO_NOMES[TIPO_LICITACAO]),
        (TIPO_DISPENSA_LICITACAO, TIPO_NOMES[TIPO_DISPENSA_LICITACAO]),
        (TIPO_INEXIGIBILIDADE_LICITACAO, TIPO_NOMES[TIPO_INEXIGIBILIDADE_LICITACAO]),
    )

    historico = AuditlogHistoryField()
    numero = models.CharField('Número do Edital', max_length=50, unique=True)
    processo = models.CharField(max_length=19, default='')
    tipo_contratacao = models.CharField(max_length=25, choices=TIPO_CONTRATACAO_CHOICES, default=TIPO_LICITACAO)
    subtipo = models.TextField(blank=True, default='')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default=ATIVO)
    data_homologacao = models.DateField('Data de homologação', blank=True, null=True)
    objeto = models.ForeignKey(TipoServico, related_name='objetos', verbose_name='Categoria de objeto',
                               on_delete=models.PROTECT, blank=True, null=True)
    descricao_objeto = models.TextField(blank=True, default='')

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'Edital'
        verbose_name_plural = 'Editais'

    @classmethod
    def tipo_contratacao_to_json(cls):
        result = []
        for tipo_contratacao in cls.TIPO_CONTRATACAO_CHOICES:
            choice = {
                'id': tipo_contratacao[0],
                'nome': tipo_contratacao[1]
            }
            result.append(choice)
        return result


auditlog.register(Edital)
