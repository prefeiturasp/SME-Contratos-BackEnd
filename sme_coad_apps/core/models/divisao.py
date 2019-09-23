from django.db import models

from ..models_abstracts import TemNome, ModeloBase


class Divisao(ModeloBase, TemNome):
    sigla = models.CharField('Sigla', max_length=15)

    def __str__(self):
        return f'{self.sigla}-{self.nome}'

    class Meta:
        verbose_name = 'Divisão'
        verbose_name_plural = 'Divisões'
