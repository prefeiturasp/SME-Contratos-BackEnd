import datetime

from django.db import models
from notifications.signals import notify

from .contrato import Contrato
from .parametro_notificacoes import ParametroNotificacoesVigencia
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

    @classmethod
    def gera_notificacoes(cls):
        for estado in Contrato.ESTADOS:

            if not ParametroNotificacoesVigencia.estado_notificavel(estado):
                continue

            data_limite = ParametroNotificacoesVigencia.data_limite_do_estado(estado)

            contratos = Contrato.contratos_no_estado(estado, vencendo_ate=data_limite)

            for contrato in contratos:
                if not contrato.gestor:
                    continue

                frequencia_de_notificacao = ParametroNotificacoesVigencia.frequencia_repeticao(
                    estado, dias_pra_vencer=contrato.dias_para_o_encerramento
                )

                ultima_notificacao = NotificacaoVigenciaContrato.ultima_notificacao_para_o_gestor_do_contrato(contrato)

                if not ultima_notificacao or ultima_notificacao.idade >= frequencia_de_notificacao:
                    notificacao = NotificacaoVigenciaContrato.objects.create(
                        contrato=contrato,
                        notificado=contrato.gestor,
                    )

                    notify.send(
                        notificacao,
                        verb='alerta_vigencia_contrato',
                        recipient=notificacao.notificado,
                        description=f'O contrato {contrato.termo_contrato} '
                                    f'está a {contrato.dias_para_o_encerramento} de seu encerramento.',
                        target=contrato,
                    )

                    if ultima_notificacao:
                        ultima_notificacao.delete()

    @classmethod
    def get_notificacoes_do_usuario(cls, usuario):
        return usuario.notifications.unread().filter(verb='alerta_vigencia_contrato')

    class Meta:
        verbose_name = 'Notificação de vigência de contrato'
        verbose_name_plural = 'Notificações de vigência de contrato'
