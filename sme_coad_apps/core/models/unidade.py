from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.core.validators import MinLengthValidator
from django.db import models

from ..models_abstracts import ModeloBase, TemNome


class Unidade(ModeloBase, TemNome):
    historico = AuditlogHistoryField(pk_indexable=False)

    # Equipamentos Choice
    EQP_UNIDADE_ADMINISTRATIVA = 'UA'
    EQP_UNIDADE_ENSINO = 'UE'
    EQP_UNIDADE_CEU = 'CEU'

    EQP_NOMES = {
        EQP_UNIDADE_ADMINISTRATIVA: 'Unidade Administrativa',
        EQP_UNIDADE_ENSINO: 'Unidade de Ensino',
        EQP_UNIDADE_CEU: 'Centro Educacional Unificado'
    }

    EQP_CHOICES = (
        (EQP_UNIDADE_ADMINISTRATIVA, EQP_NOMES[EQP_UNIDADE_ADMINISTRATIVA]),
        (EQP_UNIDADE_ENSINO, EQP_NOMES[EQP_UNIDADE_ENSINO]),
        (EQP_UNIDADE_CEU, EQP_NOMES[EQP_UNIDADE_CEU]),
    )

    equipamento = models.CharField(max_length=3, choices=EQP_CHOICES, default=EQP_UNIDADE_ENSINO)
    tipo_unidade = models.CharField(max_length=20, blank=True)
    codigo_eol = models.CharField(max_length=6, validators=[MinLengthValidator(6)], primary_key=True, unique=True)
    logradouro = models.CharField(max_length=100, blank=True, default='')
    bairro = models.CharField(max_length=50, blank=True, default='')
    dre = models.CharField(max_length=100, blank=True, default='')

    @classmethod
    def get_equipamento_from_unidade(self, unidade):
        if unidade.get('cd_tp_equipamento') == 3:
            if unidade.get('cd_tp_ua') == 19:
                return self.EQP_UNIDADE_CEU
            else:
                return self.EQP_UNIDADE_ADMINISTRATIVA
        else:
            return self.EQP_UNIDADE_ENSINO

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'


auditlog.register(Unidade)
