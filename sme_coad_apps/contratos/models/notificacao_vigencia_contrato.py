from django.db import models

from .contrato import Contrato
from ...core.models_abstracts import ModeloBase
from ...users.models import User


class NotificacaoVigenciaContrato(ModeloBase):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name="notificacoes_vigencia")
    notificado = models.ForeignKey(User, on_delete=models.PROTECT, related_name='notificacoes_vigencia', blank=True,
                                   null=True)
    validade = models.DateField('validade da notificação')

    def __str__(self):
        return f'TC:{self.contrato.termo_contrato} Notificado:{self.notificado.username} Validade:{self.validade}'

    class Meta:
        verbose_name = 'Notificação de vigência de contrato'
        verbose_name_plural = 'Notificações de vigência de contrato'
