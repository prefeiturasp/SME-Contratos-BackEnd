import datetime

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from dateutil.relativedelta import relativedelta
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from notifications.models import Notification
from notifications.signals import notify

from sme_coad_apps.core.helpers.enviar_email import enviar_email
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

    ESTADOS = (
        ESTADO_EMERGENCIAL,
        ESTADO_EXCEPCIONAL,
        ESTADO_ULTIMO_ANO,
        ESTADO_VIGENTE
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

    termo_contrato = models.CharField('TC No.', max_length=20, unique=True)
    processo = models.CharField(max_length=50, blank=True, default='')
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.PROTECT, related_name='contratos_do_tipo',
                                     verbose_name='tipo de serviço', blank=True, null=True)
    nucleo_responsavel = models.ForeignKey(Nucleo, on_delete=models.PROTECT, related_name='contratos_do_nucleo',
                                           verbose_name='núcleo responsável', blank=True, null=True)
    objeto = models.TextField(blank=True, default='')
    empresa_contratada = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='contratos_da_empresa',
                                           blank=True, null=True)
    data_assinatura = models.DateField('data da assinatura', blank=True, null=True)
    data_ordem_inicio = models.DateField('data da ordem de início', blank=True, null=True)
    vigencia_em_dias = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    situacao = models.CharField(max_length=15, choices=SITUACAO_CHOICES, default=SITUACAO_RASCUNHO)
    gestor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_geridos', blank=True,
                               null=True)
    suplente = models.ForeignKey(User, on_delete=models.PROTECT, related_name='contratos_geridos_suplente',
                                 blank=True,
                                 null=True)
    observacoes = models.TextField(blank=True, default='')
    estado_contrato = models.CharField('estado', max_length=15, choices=ESTADO_CHOICES, blank=True, default='')
    data_encerramento = models.DateField(blank=True, null=True)
    tem_ue = models.BooleanField(default=False)
    tem_ua = models.BooleanField(default=False)
    tem_ceu = models.BooleanField(default=False)
    dotacao_orcamentaria = ArrayField(models.CharField('Dotação Orçamentária', max_length=200), blank=True,
                                      default=list)

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
        return self.termo_contrato

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

    @classmethod
    def contratos_no_estado(cls, estado, vencendo_ate=None):
        result_query = cls.objects.filter(estado_contrato=estado)

        if vencendo_ate:
            result_query = result_query.filter(data_encerramento__lte=vencendo_ate)

        return result_query.all()

    @classmethod
    def notifica_atribuicao(cls, notificado, papel, contrato):
        verb = f'tc_atribuido_{papel}'
        notificacoes_lidas = notificado.notifications.read().filter(verb=verb, actor_object_id=contrato.id)
        notificacoes_nao_lidas = notificado.notifications.unread().filter(verb=verb, actor_object_id=contrato.id)

        if (not notificacoes_lidas.exists()) and (not notificacoes_nao_lidas.exists()):
            notify.send(
                contrato,
                verb=verb,
                recipient=notificado,
                description=f'Atenção! Você foi definido como {papel} do contrato {contrato.termo_contrato}.',
                target=contrato,
            )

    def notificar_gestor_e_suplente(self):
        if self.gestor:
            Contrato.notifica_atribuicao(notificado=self.gestor, papel='gestor', contrato=self)

        if self.suplente:
            Contrato.notifica_atribuicao(notificado=self.suplente, papel='suplente', contrato=self)

        Contrato.enviar_emails_notificacao()

    @classmethod
    def enviar_emails_notificacao(cls):
        notificacoes_pendentes = Notification.objects.unsent() \
            .filter(Q(verb='tc_atribuido_gestor') | Q(verb='tc_atribuido_suplente'))
        for notificacao in notificacoes_pendentes:
            assunto = f'Alerta de atribuição. Contrato:{notificacao.target.termo_contrato}'
            print(assunto)
            enviar_email(
                assunto,
                notificacao.description,
                notificacao.recipient.email
            )
            notificacao.emailed = True
            notificacao.save()

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


@receiver(post_save, sender=Contrato)
def contrato_post_save(instance, **kwargs):
    if instance.gestor:
        instance.notificar_gestor_e_suplente()


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


class ContratoUnidade(ModeloBase):
    historico = AuditlogHistoryField()

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="unidades")
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="contratos", to_field="codigo_eol")
    valor_mensal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
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
auditlog.register(DocumentoFiscal)
