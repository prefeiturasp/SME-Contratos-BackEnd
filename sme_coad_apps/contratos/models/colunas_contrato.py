from ...core.models_abstracts import ModeloBase
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

model_user = get_user_model()


class ColunasContrato(ModeloBase):
    CAMPOS = [
        {
            "field": "termo_contrato",
            "header": "TC"
        },
        {
            "field": "processo",
            "header": "Processo"
        },
        {
            "field": "tipo_servico.nome",
            "header": "Tipode de Serviço"
        },
        {
            "field": "empresa_contratada.nome",
            "header": "Empresa"
        },
        {
            "field": "estado_contrato",
            "header": "Estado do Contrato"
        },
        {
            "field": "data_encerramento",
            "header": "Data Encerramento"
        }
    ]

    usuario = models.ForeignKey(model_user, on_delete=models.PROTECT, related_name='usuario_servidor')
    colunas_array = JSONField('Lista de campos', blank=True, default=CAMPOS)

    def __str__(self):
        return self.usuario.nome

    class Meta:
        verbose_name = 'Colunas do Usuário'
        verbose_name_plural = 'Colunas do Usuário'
