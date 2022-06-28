import datetime
import json

import environ
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from notifications.models import Notification
from notifications.signals import notify
from rest_framework import viewsets
from rest_framework.response import Response

from sme_coad_apps.core.helpers.enviar_email import enviar_email_html

from ...core.models import Nucleo, Unidade
from ...core.models_abstracts import ModeloBase, TemNome
from ...users.models import User
from .ata import Ata
from .edital import Edital
from .empresa import Empresa
from .objeto import Objeto

env = environ.Env()


class SafiToken(viewsets.ViewSet):

    def list(self, request):
        return Response({'safi_token': env('SAFI_TOKEN')})


class Contrato(ModeloBase):
    historico = AuditlogHistoryField()

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

    # Referência para data de encerramento
    REFERENCIA_DATA_ASSINATURA = 'DATA_ASSINATURA'
    REFERENCIA_DATA_ORDEM_INICIO = 'DATA_ORDEM_INICIO'

    REFERENCIA_NOMES = {
        REFERENCIA_DATA_ASSINATURA: 'Data de Assinatura',
        REFERENCIA_DATA_ORDEM_INICIO: 'Data de Ordem de Inicio',
    }

    REFERENCIA_CHOICES = (
        (REFERENCIA_DATA_ASSINATURA, REFERENCIA_NOMES[REFERENCIA_DATA_ASSINATURA]),
        (REFERENCIA_DATA_ORDEM_INICIO, REFERENCIA_NOMES[REFERENCIA_DATA_ORDEM_INICIO]),
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

    termo_contrato = models.CharField('TC No.', max_length=20, unique=True)
    processo = models.CharField(max_length=50, blank=True, default='')
    edital = models.ForeignKey(Edital, on_delete=models.PROTECT, related_name='contratos_do_edital',
                               blank=True, null=True)
    ata = models.ForeignKey(Ata, on_delete=models.PROTECT, related_name='contratos_da_ata',
                            blank=True, null=True)
    objeto = models.ForeignKey(Objeto, on_delete=models.PROTECT, related_name='contratos_do_tipo',
                               verbose_name='objeto', blank=True, null=True)
    nucleo_responsavel = models.ForeignKey(Nucleo, on_delete=models.PROTECT, related_name='contratos_do_nucleo',
                                           verbose_name='núcleo responsável', blank=True, null=True)
    descricao_objeto = models.TextField(blank=True, default='')
    empresa_contratada = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='contratos_da_empresa',
                                           blank=True, null=True)
    data_assinatura = models.DateField('data da assinatura', blank=True, null=True)
    data_ordem_inicio = models.DateField('data da ordem de início', blank=True, null=True)
    referencia_encerramento = models.CharField(max_length=20, choices=REFERENCIA_CHOICES,
                                               default=REFERENCIA_DATA_ORDEM_INICIO)
    unidade_vigencia = models.CharField(max_length=10, choices=UNIDADE_VIGENCIA_CHOICES,
                                        default=UNIDADE_VIGENCIA_DIAS)
    vigencia = models.PositiveSmallIntegerField('vigência', default=0, blank=True, null=True)
    situacao = models.CharField(max_length=15, choices=SITUACAO_CHOICES, default=SITUACAO_RASCUNHO)
    observacoes = models.TextField(blank=True, default='')
    data_encerramento = models.DateField(blank=True, null=True)
    tem_ue = models.BooleanField(default=False)
    tem_ua = models.BooleanField(default=False)
    tem_ceu = models.BooleanField(default=False)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    # coordenador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_coordenador', blank=True,
    #                                 null=True)

    @property
    def dias_para_o_encerramento(self):
        if self.data_encerramento:
            dias = (self.data_encerramento - datetime.date.today()).days
            if dias > 0:
                return dias
            else:
                return 0
        else:
            return 0

    @property
    def total_mensal(self):
        total = 0
        for unidade in self.unidades.all():
            total += unidade.valor_mensal
        return total

    @property
    def dres(self):
        return ', '.join(list(filter(None, self.lotes.values_list('unidades__dre', flat=True).distinct())))

    def __str__(self):
        return self.termo_contrato

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

    @classmethod
    def notifica_atribuicao(cls, notificado, papel, contrato):
        verb = f'tc_atribuido_{papel}'
        notificacoes_lidas = notificado.notifications.read().filter(verb=verb, actor_object_id=contrato.id)
        notificacoes_nao_lidas = notificado.notifications.unread().filter(verb=verb, actor_object_id=contrato.id)

        if (not notificacoes_lidas.exists()) and (not notificacoes_nao_lidas.exists()):
            env = environ.Env()
            url = f'https://{env("SERVER_NAME")}/#/cadastro-unico-contrato/?uuid={contrato.uuid}'
            link = f'<a target="blank" href="{url}">incluir contrato</a>'
            notify.send(
                contrato,
                verb=verb,
                recipient=notificado,
                description=f'Atenção! Você foi definido como {papel} do contrato {contrato.termo_contrato}. '
                            f'Você pode acessá-lo por esse link: {link}',
                target=contrato,
                papel=papel,
                url_contrato=url
            )

    def notificar_gestor_e_suplente(self):
        if self.gestor:
            Contrato.notifica_atribuicao(notificado=self.gestor, papel='gestor', contrato=self)

        if self.suplente:
            Contrato.notifica_atribuicao(notificado=self.suplente, papel='suplente', contrato=self)

        Contrato.enviar_emails_notificacao()

    @classmethod
    def enviar_emails_notificacao(cls):
        notificacoes_pendentes = Notification.objects.unsent().filter(
            Q(verb='tc_atribuido_gestor') | Q(verb='tc_atribuido_suplente'))
        for notificacao in notificacoes_pendentes:
            if type(notificacao.data) is dict:
                papel = notificacao.data['papel']
                url_contrato = notificacao.data['url_contrato']
            else:
                papel = json.loads(notificacao.data)['papel']
                url_contrato = json.loads(notificacao.data)['url_contrato']
            assunto = f'Alerta de atribuição. Contrato:{notificacao.target.termo_contrato}'

            enviar_email_html(
                assunto,
                'email_atribuicao_contrato',
                {'nome': notificacao.recipient.first_name,
                 'papel': papel,
                 'contrato': notificacao.target.termo_contrato,
                 'url_contrato': url_contrato,
                 'mensagem': notificacao.description,
                 },
                notificacao.recipient.email
            )
            notificacao.emailed = True
            notificacao.save()

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'


@receiver(pre_save, sender=Contrato)
def contrato_pre_save(instance, *_args, **_kwargs):
    if instance.referencia_encerramento == Contrato.REFERENCIA_DATA_ASSINATURA:
        data_inicio = instance.data_assinatura
    else:
        data_inicio = instance.data_ordem_inicio

    if data_inicio and instance.vigencia:
        if instance.unidade_vigencia == Contrato.UNIDADE_VIGENCIA_MESES:
            instance.data_encerramento = data_inicio + relativedelta(months=+instance.vigencia) - relativedelta(
                days=+1)
        else:
            instance.data_encerramento = data_inicio + relativedelta(days=+instance.vigencia)

    instance.tem_ue = instance.unidades.filter(unidade__equipamento='UE').exists()
    instance.tem_ua = instance.unidades.filter(unidade__equipamento='UA').exists()
    instance.tem_ceu = instance.unidades.filter(unidade__equipamento='CEU').exists()
    if instance.data_encerramento and instance.data_assinatura:
        instance.data_assinatura += relativedelta(days=+1)
    if instance.data_encerramento and instance.data_ordem_inicio:
        instance.data_ordem_inicio += relativedelta(days=+1)


class DocumentoFiscal(ModeloBase):
    historico = AuditlogHistoryField()

    CHOICES = (('FISCAL_DRE', 'DRE'), ('FISCAL_UNIDADE', 'UNIDADE'), ('FISCAL_OUTROS', 'OUTROS'))
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='documentos_fiscais')
    anexo = models.FileField(upload_to='uploads/')
    tipo_unidade = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return f'{self.contrato.termo_contrato} - {self.tipo_unidade}'

    class Meta:
        verbose_name = 'Documento Fiscal'
        verbose_name_plural = 'Documentos Fiscais'


class Lote(ModeloBase, TemNome):
    historico = AuditlogHistoryField()

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='lotes')
    unidades = models.ManyToManyField(Unidade)

    def __str__(self):
        return f'Lote {self.nome}'

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'


class FiscalLote(ModeloBase):
    # Tipos de Fiscal
    FISCAL_TITULAR = 'TITULAR'
    FISCAL_SUPLENTE = 'SUPLENTE'

    FISCAL_NOMES = {
        FISCAL_TITULAR: 'Titular',
        FISCAL_SUPLENTE: 'Suplente',
    }

    FISCAL_CHOICES = (
        (FISCAL_TITULAR, FISCAL_NOMES[FISCAL_TITULAR]),
        (FISCAL_SUPLENTE, FISCAL_NOMES[FISCAL_SUPLENTE]),
    )

    historico = AuditlogHistoryField()

    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='fiscais_lote', blank=True,
                             null=True)
    fiscal = models.ForeignKey(User, on_delete=models.PROTECT, related_name='fiscais')
    tipo_fiscal = models.CharField(max_length=15, choices=FISCAL_CHOICES, default=FISCAL_SUPLENTE)

    def __str__(self):
        return f'{self.fiscal.nome} do {self.lote.nome}'

    class Meta:
        verbose_name = 'Fiscal do Lote de Contrato'
        verbose_name_plural = 'Fiscais dos Lotes de Contratos'


class ContratoUnidade(ModeloBase):
    historico = AuditlogHistoryField()

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='unidades')
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name='contratos', to_field='codigo_eol')
    valor_mensal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    lote = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return f'TC:{self.contrato.termo_contrato} - Unidade: {self.unidade.nome}'

    @property
    def numero_lote(self):
        return f'Lote {self.lote}'

    @property
    def fiscais(self):
        return self.fiscais

    class Meta:
        verbose_name = 'Unidade de Contrato'
        verbose_name_plural = 'Unidades de Contratos'


class FiscaisUnidade(ModeloBase):
    # Tipos de Fiscal
    FISCAL_TITULAR = 'TITULAR'
    FISCAL_SUPLENTE = 'SUPLENTE'

    FISCAL_NOMES = {
        FISCAL_TITULAR: 'Titular',
        FISCAL_SUPLENTE: 'Suplente',
    }

    FISCAL_CHOICES = (
        (FISCAL_TITULAR, FISCAL_NOMES[FISCAL_TITULAR]),
        (FISCAL_SUPLENTE, FISCAL_NOMES[FISCAL_SUPLENTE]),
    )

    historico = AuditlogHistoryField()

    contrato_unidade = models.ForeignKey(ContratoUnidade, on_delete=models.CASCADE, related_name='fiscais', blank=True,
                                         null=True)
    fiscal = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_fiscalizados')
    tipo_fiscal = models.CharField(max_length=15, choices=FISCAL_CHOICES, default=FISCAL_SUPLENTE)

    def __str__(self):
        contrato = ''
        unidade = ''
        fiscal = f'Fiscal ({self.tipo_fiscal}): {self.fiscal.nome}'
        if self.contrato_unidade:
            contrato = f'TC:{self.contrato_unidade.contrato.termo_contrato}'
            unidade = f'unidade: {self.contrato_unidade.unidade.nome}'
        return f'{fiscal} do {contrato} na {unidade}'

    class Meta:
        verbose_name = 'Fiscal da Unidade de Contrato'
        verbose_name_plural = 'Fiscais das Unidades de Contratos'


class GestorContrato(ModeloBase):
    historico = AuditlogHistoryField()

    gestor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_geridos', blank=True,
                               null=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name='gestores')

    def __str__(self):
        return f'{self.contrato.termo_contrato} - {self.gestor.nome}'

    class Meta:
        verbose_name = 'Gestor de Contrato'
        verbose_name_plural = 'Gestores de Contrato'


auditlog.register(Contrato)
auditlog.register(ContratoUnidade)
auditlog.register(DocumentoFiscal)
auditlog.register(FiscaisUnidade)
auditlog.register(GestorContrato)
