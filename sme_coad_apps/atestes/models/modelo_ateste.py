from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ...core.models_abstracts import ModeloBase


class ModeloAteste(ModeloBase):
    historico = AuditlogHistoryField()
    titulo = models.CharField('Titulo do Modelo', max_length=100)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Modelo de Ateste'
        verbose_name_plural = 'Modelos de Atestes'


class GrupoVerificacao(ModeloBase):
    historico = AuditlogHistoryField()
    nome = models.CharField('Nome do Grupo', max_length=100)
    modelo = models.ForeignKey(ModeloAteste, on_delete=models.CASCADE, related_name="grupos_de_verificacao")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Grupo de Verificacao'
        verbose_name_plural = 'Grupos de verificação'


class ItensVerificacao(ModeloBase):
    historico = AuditlogHistoryField()
    descricao = models.TextField('Descrição')
    item = models.SmallIntegerField('Item', default=0)
    grupo = models.ForeignKey(GrupoVerificacao, on_delete=models.CASCADE, related_name="itens_de_verificacao")

    def __str__(self):
        return f'{self.item} - {self.descricao}'

    class Meta:
        verbose_name = 'Item de Verificação'
        verbose_name_plural = 'Itens de Verificação'


@receiver(pre_save, sender=ItensVerificacao)
def itens_pre_save(instance, *_args, **_kwargs):
    if not instance.item:
        if ItensVerificacao.objects.exists():
            instance.item = ItensVerificacao.objects.latest('item').item + 1
        else:
            instance.item = 1


auditlog.register(ModeloAteste)
auditlog.register(GrupoVerificacao)
auditlog.register(ItensVerificacao)
