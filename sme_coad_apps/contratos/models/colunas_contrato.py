from ...core.models_abstracts import ModeloBase
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField

model_user = get_user_model()


class ColunasContrato(ModeloBase):
    CAMPOS = [
        {
            "field": "termo_contrato",
            "header": "TC",
            "checked": True
        },
        {
            "field": "processo",
            "header": "Processo",
            "checked": True
        },
        {
            "field": "tipo_servico.nome",
            "header": "Tipode de Serviço",
            "checked": True
        },
        {
            "field": "empresa_contratada.nome",
            "header": "Empresa",
            "checked": True
        },
        {
            "field": "estado_contrato",
            "header": "Estado do Contrato",
            "checked": True
        },
        {
            "field": "data_encerramento",
            "header": "Data Encerramento",
            "checked": True
        },
        {
            "field": "nucleo_responsavel",
            "header": "Núcleo Responsável",
            "checked": False
        },
        {
            "field": "objeto",
            "header": "Objeto",
            "checked": False
        },
        {
            "field": "data_assinatura",
            "header": "Data Assinatura",
            "checked": False
        },
        {
            "field": "data_ordem_inicio",
            "header": "Data Ordem de Inicio",
            "checked": False
        },
        {
            "field": "vigencia_em_dias",
            "header": "Vigencia",
            "checked": False
        },
        {
            "field": "situacao",
            "header": "Situação",
            "checked": False
        },
        {
            "field": "gestor",
            "header": "Gestor",
            "checked": False
        },
        {
            "field": "suplente",
            "header": "Suplente",
            "checked": False
        },
        {
            "field": "observacoes",
            "header": "Observações",
            "checked": False
        }
    ]

    usuario = models.ForeignKey(model_user, on_delete=models.PROTECT, related_name='usuario_servidor')
    colunas_array = ArrayField(models.CharField('Lista de campos', max_length=200), blank=True, default=CAMPOS)

    def __str__(self):
        return self.usuario.nome

    class Meta:
        verbose_name = 'Colunas do Usuário'
        verbose_name_plural = 'Colunas do Usuário'
