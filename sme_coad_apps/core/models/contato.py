from django.core.validators import MinLengthValidator
from django.db import models

from ...core.models_abstracts import ModeloBase


class Contato(ModeloBase):
    nome = models.CharField('Nome', max_length=160, blank=True)
    rg = models.CharField(max_length=75, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(
        max_length=13, validators=[MinLengthValidator(10)], blank=True
    )
    cargo = models.CharField(max_length=75, blank=True)

    def __str__(self):
        if self.nome and self.telefone and self.email:
            return f'{self.nome}, {self.telefone}, {self.email}'
        elif self.nome:
            return self.nome
