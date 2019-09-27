import datetime

from dateutil.relativedelta import relativedelta
from django.db import models

from .empresa import Empresa
from .tipo_servico import TipoServico
from ...core.models import Nucleo, Unidade
from ...core.models_abstracts import ModeloBase
from ...users.models import User


class Contrato(ModeloBase):
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

    SITUACAO_NOMES = {
        SITUACAO_ATIVO: 'Ativo',
        SITUACAO_ENCERRADO: 'Encerrado',
    }

    SITUACAO_CHOICES = (
        (SITUACAO_ATIVO, SITUACAO_NOMES[SITUACAO_ATIVO]),
        (SITUACAO_ENCERRADO, SITUACAO_NOMES[SITUACAO_ENCERRADO]),
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
    observacoes = models.TextField(blank=True, default='')
    estado_contrato = models.CharField('estado', max_length=15, choices=ESTADO_CHOICES, default=ESTADO_VIGENTE)

    @property
    def data_encerramento(self):
        if self.vigencia_em_dias and self.data_ordem_inicio:
            return self.data_ordem_inicio + relativedelta(days=+self.vigencia_em_dias)
        return ''

    @property
    def dias_para_o_encerramento(self):
        return (self.data_encerramento - datetime.date.today()).days

    @property
    def estado(self):
        # Futuramente o estado será calculado. No momento ele é um campo digitado.
        return self.estado_contrato

    def __str__(self):
        return f'TC:{self.termo_contrato} - {self.tipo_servico.nome} - {Contrato.SITUACAO_NOMES[self.situacao]}'

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'


class ContratoUnidade(ModeloBase):
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
