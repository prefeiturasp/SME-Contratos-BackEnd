from django.contrib.postgres.fields import JSONField
from django.db import models

from ..core.models_abstracts import ModeloBase


class RequisicaoApiSofi(ModeloBase):
    # Status da requisição
    SUCESSO = 'SUCESSO'
    ERRO = 'ERRO'

    STATUS_CHOICES = (
        (SUCESSO, 'Sucesso'),
        (ERRO, 'Erro'),
    )
    endpoint = models.CharField(max_length=50)
    data = models.DateTimeField(editable=False, auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, blank=True, default='')
    resultado = JSONField(blank=True, default=dict)

    def __str__(self):
        return self.endpoint

    class Meta:
        verbose_name = 'Requisição da API Sofi'
        verbose_name_plural = 'Requisições da API Sofi'

    @classmethod
    def criar_requisicao(cls, endpoint):
        requisicao = cls.objects.create(endpoint=endpoint)

        return requisicao
