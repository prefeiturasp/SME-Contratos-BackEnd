from django.db import models

from ...core.models_abstracts import ModeloBase, TemNome


class TipoServico(ModeloBase, TemNome):

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Tipo de Serviço'
        verbose_name_plural = 'Tipos de Serviço'

