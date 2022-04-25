from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from brazilnum.cnpj import format_cnpj
from django.core.validators import MinLengthValidator
from django.db import models

from ...core.models.contato import Contato
from ...core.models_abstracts import ModeloBase, TemNome


class Empresa(ModeloBase, TemNome):
    # Situações da Empresa Choice
    SITUACAO_ATIVA = 'ATIVA'
    SITUACAO_INATIVA = 'INATIVA'

    SITUACAO_CHOICES = (
        (SITUACAO_ATIVA, 'Ativa'),
        (SITUACAO_INATIVA, 'Inativa'),
    )
    # Tipo de Serviço Choice
    ARMAZEM_DISTRIBUIDOR = 'ARMAZEM/DISTRIBUIDOR'
    FORNECEDOR_DISTRIBUIDOR = 'FORNECEDOR/DISTRIBUIDOR'
    FORNECEDOR = 'FORNECEDOR'

    TIPO_SERVICO_CHOICES = (
        (ARMAZEM_DISTRIBUIDOR, 'Armazém/Distribuidor'),
        (FORNECEDOR_DISTRIBUIDOR, 'Fornecedor/Distribuidor'),
        (FORNECEDOR, 'Fornecedor'),
    )
    # Tipo de Fornecedor Choice
    AGRICULTURA_FAMILIAR = 'AGRICULTURA_FAMILIAR'
    CONVENCIONAL = 'CONVENCIONAL'

    TIPO_FORNECEDOR_CHOICES = (
        (AGRICULTURA_FAMILIAR, 'Agricultura familiar'),
        (CONVENCIONAL, 'CONVENCIONAL'),
    )

    historico = AuditlogHistoryField()

    # TODO Implementar validação do CNPJ para não permitir gravação de CNPJ inválido.
    cnpj = models.CharField('CNPJ', validators=[MinLengthValidator(14)], max_length=14, unique=True)
    razao_social = models.CharField('Razão Social', max_length=160, blank=True)
    tipo_servico = models.CharField(choices=TIPO_SERVICO_CHOICES, max_length=25, default=ARMAZEM_DISTRIBUIDOR)
    tipo_fornecedor = models.CharField(choices=TIPO_FORNECEDOR_CHOICES, max_length=25, blank=True, default='')
    situacao = models.CharField(choices=SITUACAO_CHOICES, max_length=25, blank=True, default=SITUACAO_ATIVA)

    cep = models.CharField('CEP', max_length=8, blank=True)
    endereco = models.CharField('Endereco', max_length=160, blank=True)
    bairro = models.CharField('Bairro', max_length=150, blank=True)
    cidade = models.CharField('Cidade', max_length=150, blank=True)
    estado = models.CharField('Estado', max_length=150, blank=True)
    numero = models.CharField('Número', max_length=10, blank=True)
    complemento = models.CharField('Complemento', max_length=100, blank=True)

    contatos = models.ManyToManyField(Contato, blank=True)

    def __str__(self):
        return self.nome

    @property
    def cnpj_formatado(self):
        return format_cnpj(self.cnpj)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


auditlog.register(Empresa)
