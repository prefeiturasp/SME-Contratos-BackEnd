from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class Intercorrencia(ModeloBase):
    # Tipo Intercorrência
    TIPO_INTERCORRENCIA_SUSPENSAO = 'SUSPENSAO'
    TIPO_INTERCORRENCIA_IMPEDIMENTO = 'IMPEDIMENTO'
    TIPO_INTERCORRENCIA_RESCISAO = 'RESCISAO'

    TIPO_NOMES = {
        TIPO_INTERCORRENCIA_SUSPENSAO: 'Suspensão',
        TIPO_INTERCORRENCIA_IMPEDIMENTO: 'Impedimento',
        TIPO_INTERCORRENCIA_RESCISAO: 'Rescisão',
    }

    TIPO_CHOICES = (
        (TIPO_INTERCORRENCIA_SUSPENSAO, TIPO_NOMES[TIPO_INTERCORRENCIA_SUSPENSAO]),
        (TIPO_INTERCORRENCIA_IMPEDIMENTO, TIPO_NOMES[TIPO_INTERCORRENCIA_IMPEDIMENTO]),
        (TIPO_INTERCORRENCIA_RESCISAO, TIPO_NOMES[TIPO_INTERCORRENCIA_RESCISAO]),
    )
    # Motivos de Suspensão
    MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA = 'UNILATERALMENTE_ADMINISTRACAO_PUBLICA'
    MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO = 'UNILATERALMENTE_CONTRATADO'
    MOTIVO_SUSPENSAO_CONSENSUALMENTE = 'CONSENSUALMENTE'

    MOTIVO_NOMES = {
        MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA: 'Unilateralmente pela Administração Pública',
        MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO: 'Unilateralmente pelo Contratado',
        MOTIVO_SUSPENSAO_CONSENSUALMENTE: 'Consensualmente',
    }

    MOTIVO_CHOICES = (
        (MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA,
         MOTIVO_NOMES[MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA]),
        (MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO, MOTIVO_NOMES[MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO]),
        (MOTIVO_SUSPENSAO_CONSENSUALMENTE, MOTIVO_NOMES[MOTIVO_SUSPENSAO_CONSENSUALMENTE]),
    )
    historico = AuditlogHistoryField()
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='intercorrencias')
    tipo_intercorrencia = models.CharField(choices=TIPO_CHOICES, max_length=25)
    data_inicial = models.DateField('Data Inicial', null=True)
    data_final = models.DateField('Data Final', null=True)
    acrescentar_dias = models.BooleanField(default=False)
    data_encerramento = models.DateField('Data de Encerramento', null=True)
    motivo_suspensao = models.CharField(choices=MOTIVO_CHOICES, max_length=50)
    opcao_suspensao = models.TextField('Opção de Suspensão', blank=True)
    descricao_suspensao = models.TextField('Descrição do Motivo', blank=True)

    @classmethod
    def motivos_suspensao_to_json(cls):
        result = []
        for motivo in cls.MOTIVO_CHOICES:
            choice = {
                'id': motivo[0],
                'nome': motivo[1]
            }
            result.append(choice)
        return result

    def __str__(self):
        return self.tipo_intercorrencia

    class Meta:
        verbose_name = 'Intercorrência'
        verbose_name_plural = 'Intercorrências'


auditlog.register(Intercorrencia)
