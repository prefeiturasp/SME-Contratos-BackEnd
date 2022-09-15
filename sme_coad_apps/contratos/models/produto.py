from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models

from ...core.models_abstracts import ModeloBase


class UnidadeDeMedida(ModeloBase):
    nome = models.CharField('Nome', max_length=160)

    def __str__(self):
        return self.nome


class Produto(ModeloBase):
    # Situações do produto Choice
    SITUACAO_ATIVO = 'ATIVO'
    SITUACAO_INATIVO = 'INATIVO'

    SITUACAO_CHOICES = (
        (SITUACAO_ATIVO, 'Ativo'),
        (SITUACAO_INATIVO, 'Inativo'),
    )
    # Categorias do produto Choice
    CATEGORIA_ALIMENTO = 'ALIMENTO'
    CATEGORIA_OUTROS = 'OUTROS'

    CATEGORIA_CHOICES = (
        (CATEGORIA_ALIMENTO, 'Alimento'),
        (CATEGORIA_OUTROS, 'Outro(s)'),
    )

    # Tipo de Programa do produto Choice
    TIPO_PROGRAMA_ALIMENTACAO_ESCOLAR = 'ALIMENTACAO_ESCOLAR'
    TIPO_PROGRAMA_LEVE_LEITE = 'LEVE_LEITE'

    TIPO_PROGRAMA_CHOICES = (
        (TIPO_PROGRAMA_ALIMENTACAO_ESCOLAR, 'Alimentação Escolar'),
        (TIPO_PROGRAMA_LEVE_LEITE, 'Leve Leite'),
    )

    # Grupo alimentar Choice
    GRUPO_ALIMENTAR_CONGELADOS = 'CONGELADOS_E_RESFRIADOS'
    GRUPO_ALIMENTAR_FLVO = 'FLVO'
    GRUPO_ALIMENTAR_PAES_E_BOLO = 'PAES_E_BOLO'
    GRUPO_ALIMENTAR_SECOS = 'SECOS'

    GRUPO_ALIMENTAR_NOMES = {
        GRUPO_ALIMENTAR_CONGELADOS: 'Congelados e resfriados',
        GRUPO_ALIMENTAR_FLVO: 'FLVO',
        GRUPO_ALIMENTAR_PAES_E_BOLO: 'Pães e bolos',
        GRUPO_ALIMENTAR_SECOS: 'Secos',

    }

    GRUPO_ALIMENTAR_CHOICES = (
        (GRUPO_ALIMENTAR_CONGELADOS, GRUPO_ALIMENTAR_NOMES[GRUPO_ALIMENTAR_CONGELADOS]),
        (GRUPO_ALIMENTAR_FLVO, GRUPO_ALIMENTAR_NOMES[GRUPO_ALIMENTAR_FLVO]),
        (GRUPO_ALIMENTAR_PAES_E_BOLO, GRUPO_ALIMENTAR_NOMES[GRUPO_ALIMENTAR_PAES_E_BOLO]),
        (GRUPO_ALIMENTAR_SECOS, GRUPO_ALIMENTAR_NOMES[GRUPO_ALIMENTAR_SECOS]),
    )

    historico = AuditlogHistoryField()

    nome = models.CharField('Nome', max_length=160, unique=True)
    categoria = models.CharField(choices=CATEGORIA_CHOICES, max_length=25, blank=True, default=CATEGORIA_ALIMENTO)
    situacao = models.CharField(choices=SITUACAO_CHOICES, max_length=25, default=SITUACAO_ATIVO)
    grupo_alimentar = models.CharField(choices=GRUPO_ALIMENTAR_CHOICES, max_length=25, blank=True, default='')
    tipo_programa = models.CharField(choices=TIPO_PROGRAMA_CHOICES, max_length=25, blank=True, default='')
    unidade_medida = models.ForeignKey(UnidadeDeMedida, on_delete=models.PROTECT, related_name='produtos')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.nome = self.nome.upper()
        super(Produto, self).save(force_insert, force_update)


auditlog.register(Produto)
