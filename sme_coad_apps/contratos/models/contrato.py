import datetime

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .empresa import Empresa
from .tipo_servico import TipoServico
from ...core.models import Nucleo, Unidade
from ...core.models_abstracts import ModeloBase
from ...users.models import User


class Contrato(ModeloBase):
    historico = AuditlogHistoryField()

    # Estado do Contrato
    ESTADO_EMERGENCIAL = 'EMERGENCIAL'
    ESTADO_EXCEPCIONAL = 'EXCEPCIONAL'
    ESTADO_ULTIMO_ANO = 'ULTIMO_ANO'
    ESTADO_VIGENTE = 'VIGENTE'

    ESTADO_NOMES = {
        ESTADO_EMERGENCIAL: 'Emergencial',
        ESTADO_EXCEPCIONAL: 'Excepcional',
        ESTADO_ULTIMO_ANO: 'Último Ano',
        ESTADO_VIGENTE: 'Vigente'
    }

    ESTADO_CHOICES = (
        (ESTADO_EMERGENCIAL, ESTADO_NOMES[ESTADO_EMERGENCIAL]),
        (ESTADO_EXCEPCIONAL, ESTADO_NOMES[ESTADO_EXCEPCIONAL]),
        (ESTADO_ULTIMO_ANO, ESTADO_NOMES[ESTADO_ULTIMO_ANO]),
        (ESTADO_VIGENTE, ESTADO_NOMES[ESTADO_VIGENTE]),
    )

    # Situações do Contrato Choice
    SITUACAO_ATIVO = 'ATIVO'
    SITUACAO_ENCERRADO = 'ENCERRADO'
    SITUACAO_RASCUNHO = 'RASCUNHO'

    SITUACAO_NOMES = {
        SITUACAO_ATIVO: 'Ativo',
        SITUACAO_ENCERRADO: 'Encerrado',
        SITUACAO_RASCUNHO: 'Rascunho',
    }

    SITUACAO_CHOICES = (
        (SITUACAO_ATIVO, SITUACAO_NOMES[SITUACAO_ATIVO]),
        (SITUACAO_ENCERRADO, SITUACAO_NOMES[SITUACAO_ENCERRADO]),
        (SITUACAO_RASCUNHO, SITUACAO_NOMES[SITUACAO_RASCUNHO]),
    )

    termo_contrato = models.CharField('TC No.', max_length=20)
    processo = models.CharField(max_length=50)
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.PROTECT, related_name='contratos_do_tipo',
                                     verbose_name='tipo de serviço')
    nucleo_responsavel = models.ForeignKey(Nucleo, on_delete=models.PROTECT, related_name='contratos_do_nucleo',
                                           verbose_name='núcleo responsável')
    objeto = models.TextField(blank=True, default='')
    empresa_contratada = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='contratos_da_empresa')
    data_assinatura = models.DateField('data da assinatura', blank=True, null=True)
    data_ordem_inicio = models.DateField('data da ordem de início', blank=True, null=True)
    vigencia_em_dias = models.PositiveSmallIntegerField(default=0)
    situacao = models.CharField(max_length=15, choices=SITUACAO_CHOICES, default=SITUACAO_ATIVO)
    gestor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_geridos', blank=True, null=True)
    suplente = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_geridos_suplente', blank=True,
                                 null=True)
    observacoes = models.TextField(blank=True, default='')
    estado_contrato = models.CharField('estado', max_length=15, choices=ESTADO_CHOICES, default=ESTADO_VIGENTE)
    data_encerramento = models.DateField(blank=True, null=True)
    tem_ue = models.BooleanField(default=False)
    tem_ua = models.BooleanField(default=False)
    tem_ceu = models.BooleanField(default=False)

    @property
    def dias_para_o_encerramento(self):
        if self.data_encerramento:
            return (self.data_encerramento - datetime.date.today()).days
        else:
            return 0

    @property
    def estado(self):
        # Futuramente o estado será calculado. No momento ele é um campo digitado.
        return self.estado_contrato

    @property
    def total_mensal(self):
        total = 0
        for unidade in self.unidades.all():
            total += unidade.valor_mensal
        return total

    def __str__(self):
        return f'TC:{self.termo_contrato} - {self.tipo_servico.nome} - {Contrato.SITUACAO_NOMES[self.situacao]}'

    @classmethod
    def estados_to_json(cls):
        result = []
        for estado in cls.ESTADO_CHOICES:
            choice = {
                'id': estado[0],
                'nome': estado[1]
            }
            result.append(choice)
        return result

    @classmethod
    def situacoes_to_json(cls):
        result = []
        for situacao in cls.SITUACAO_CHOICES:
            choice = {
                'id': situacao[0],
                'nome': situacao[1]
            }
            result.append(choice)
        return result

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'


@receiver(pre_save, sender=Contrato)
def contrato_pre_save(instance, *_args, **_kwargs):
    if instance.data_ordem_inicio and instance.vigencia_em_dias:
        instance.data_encerramento = instance.data_ordem_inicio + relativedelta(days=+instance.vigencia_em_dias)

    instance.tem_ue = instance.unidades.filter(unidade__equipamento='UE').exists()
    instance.tem_ua = instance.unidades.filter(unidade__equipamento='UA').exists()
    instance.tem_ceu = instance.unidades.filter(unidade__equipamento='CEU').exists()


class ContratoUnidade(ModeloBase):
    historico = AuditlogHistoryField()

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="unidades")
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="contratos", to_field="codigo_eol")
    valor_mensal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    dotacao_orcamentaria = models.CharField(max_length=20)
    lote = models.CharField(max_length=20, blank=True, default='')
    dre_lote = models.CharField('DRE do lote', max_length=5, blank=True, default='')

    def __str__(self):
        return f'TC:{self.contrato.termo_contrato} - Unidade: {self.unidade.nome}'

    @property
    def numero_lote(self):
        if self.dre_lote != '':
            return f'Lote {self.lote} DRE {self.dre_lote}'
        else:
            return f'Lote {self.lote}'

    class Meta:
        verbose_name = 'Unidade de Contrato'
        verbose_name_plural = 'Unidades de Contratos'


auditlog.register(Contrato)
auditlog.register(ContratoUnidade)
