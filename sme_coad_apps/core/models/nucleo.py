from django.db import models

from ..models_abstracts import TemNome, ModeloBase
from ..models import Divisao


class Nucleo(ModeloBase, TemNome):
    sigla = models.CharField('Sigla', max_length=20)
    divisao = models.ForeignKey(Divisao, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.divisao.sigla}/{self.sigla}-{self.nome}'

    class Meta:
        verbose_name = 'Núcleo'
        verbose_name_plural = 'Núcleos'

