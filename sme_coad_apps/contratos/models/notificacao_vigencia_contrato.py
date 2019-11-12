import datetime

from django.db import models

from .contrato import Contrato
from ...core.models_abstracts import ModeloBase
from ...users.models import User


class NotificacaoVigenciaContrato(ModeloBase):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="notificacoes_vigencia")
    notificado = models.ForeignKey(User, on_delete=models.PROTECT, related_name='notificacoes_vigencia', blank=True,
                                   null=True)

    def __str__(self):
        return f'TC:{self.contrato.termo_contrato} Notificado:{self.notificado.username}'

    @classmethod
    def ultima_notificacao_para_o_gestor_do_contrato(cls, contrato):
        notificacoes_do_gestor = cls.objects.filter(contrato=contrato, notificado=contrato.gestor).all().order_by("-id")
        return notificacoes_do_gestor[0] if notificacoes_do_gestor else None

    @classmethod
    def ultima_notificacao_para_o_suplente_do_contrato(cls, contrato):
        return cls.objects.filter(contrato=contrato, notificado=contrato.suplente).all().order_by("-id")[0]

    @property
    def idade(self):
        timedelta = datetime.date.today() - self.criado_em.date()
        return timedelta.days

    class Meta:
        verbose_name = 'Notificação de vigência de contrato'
        verbose_name_plural = 'Notificações de vigência de contrato'
