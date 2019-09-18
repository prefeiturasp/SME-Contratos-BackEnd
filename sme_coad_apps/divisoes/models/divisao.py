from django.db import models

from sme_coad_apps.core.models_abstracts import TemNome, TemAtivo, TemChaveExterna


class Divisao(TemChaveExterna, TemNome, TemAtivo):
    sigla = models.CharField('Sigla', max_length=15)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Divisão'
        verbose_name_plural = 'Divisões'
        db_table = 'divisao'
