from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...contratos.models import TipoServico
from ...core.models_abstracts import ModeloBase


class Edital(ModeloBase):

    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'

    STATUS_CHOICES = (
        (ATIVO, 'AtivO'),
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
    tipo_contratacao = models.CharField(max_length=15, choices=TIPO_CONTRATACAO_CHOICES, default=TIPO_LICITACAO)
    subtipo = models.TextField(blank=True, default='')
    outro_subtipo = models.TextField(blank=True, default='')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default=ATIVO)
    data_homologacao = models.DateField('Data de homologação', blank=True, null=True)
    categoria_objeto = models.ForeignKey(TipoServico, 'Categoria de Objeto', on_delete=models.PROTECT,
                                         related_name='objetos', verbose_name='Categoria de objeto',
                                         blank=True, null=True)
    objeto = models.TextField(blank=True, default='')

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'Edital'
        verbose_name_plural = 'Editais'


auditlog.register(Edital)
