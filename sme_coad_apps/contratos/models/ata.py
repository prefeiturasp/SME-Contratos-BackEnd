from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .edital import Edital
from .empresa import Empresa
from .produto import Produto


class Ata(ModeloBase):
    # Status da ata
    ATIVA = 'ATIVA'
    ENCERRADA = 'ENCERRADA'
    RASCUNHO = 'RASCUNHO'

    STATUS_CHOICES = (
        (ATIVA, 'Ativa'),
        (ENCERRADA, 'Encerrada'),
        (RASCUNHO, 'Rascunho'),
    )

    # Unidades de Vigência
    UNIDADE_VIGENCIA_DIAS = 'DIAS'
    UNIDADE_VIGENCIA_MESES = 'MESES'

    UNIDADE_VIGENCIA_NOMES = {
        UNIDADE_VIGENCIA_DIAS: 'dias',
        UNIDADE_VIGENCIA_MESES: 'meses',
    }

    UNIDADE_VIGENCIA_CHOICES = (
        (UNIDADE_VIGENCIA_DIAS, UNIDADE_VIGENCIA_NOMES[UNIDADE_VIGENCIA_DIAS]),
        (UNIDADE_VIGENCIA_MESES, UNIDADE_VIGENCIA_NOMES[UNIDADE_VIGENCIA_MESES]),
    )

    historico = AuditlogHistoryField()
    numero = models.CharField('Número da Ata', max_length=50, unique=True)
    edital = models.ForeignKey(Edital, on_delete=models.PROTECT, related_name='atas_do_edital', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default=RASCUNHO)
    data_assinatura = models.DateField('Data da assinatura', blank=True, null=True)
    vigencia = models.PositiveSmallIntegerField('Vigência', default=0, blank=True, null=True)
    unidade_vigencia = models.CharField(max_length=10, choices=UNIDADE_VIGENCIA_CHOICES,
                                        default=UNIDADE_VIGENCIA_DIAS)
    data_encerramento = models.DateField('Data de encerramento', blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='atas', blank=True, null=True)

    def __str__(self):
        return self.numero

    class Meta:
        verbose_name = 'Ata'
        verbose_name_plural = 'Atas'


class ProdutosAta(ModeloBase):
    historico = AuditlogHistoryField(delete_related=False)

    ata = models.ForeignKey(Ata, on_delete=models.CASCADE, related_name='produtos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produtos_ata')
    quantidade_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    anexo = models.FileField(blank=True, default='', upload_to='uploads/')

    def __str__(self):
        return f'{self.produto.nome} - {self.ata.numero}'

    class Meta:
        verbose_name = 'Produto de Ata'
        verbose_name_plural = 'Produtos de Atas'


auditlog.register(Ata)
auditlog.register(ProdutosAta)
