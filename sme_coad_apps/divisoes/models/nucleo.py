from django.db import models

from sme_coad_apps.core.models_abstracts import Nomeavel, Ativavel, Descritivel, TemChaveExterna
from sme_coad_apps.divisoes.models import Divisao


class Nucleo(TemChaveExterna, Nomeavel, Descritivel, Ativavel):
    sigla = models.CharField('Sigla', max_length=20)
    divisao = models.ForeignKey(Divisao, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Núcleo'
        verbose_name_plural = 'Núcleos'
        db_table = 'nucleo'
