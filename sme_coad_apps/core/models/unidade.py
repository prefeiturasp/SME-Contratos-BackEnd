from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ..models_abstracts import TemNome, ModeloBase


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

    # Tipo de Unidade Choices
    TIPOS_CHOICE = (
        ('ADM', 'ADM'),
        ('DRE', 'DRE'),
        ('IFSP', 'IFSP'),
        ('CMCT', 'CMCT'),
        ('CECI', 'CECI'),
        ('CEI', 'CEI'),
        ('CEMEI', 'CEMEI'),
        ('CIEJA', 'CIEJA'),
        ('EMEBS', 'EMEBS'),
        ('EMEF', 'EMEF'),
        ('EMEFM', 'EMEFM'),
        ('EMEI', 'EMEI'),
        ('CEU', 'CEU'),
    )

    equipamento = models.CharField(max_length=3, choices=EQP_CHOICES, default=EQP_UNIDADE_ENSINO)
    tipo_unidade = models.CharField(max_length=10, choices=TIPOS_CHOICE, default='ADM')
    codigo_eol = models.CharField(max_length=10, primary_key=True, unique=True)
    cep = models.CharField(max_length=15, blank=True, default='')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'


auditlog.register(Unidade)
