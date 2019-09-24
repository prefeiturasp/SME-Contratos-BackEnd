import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from sme_coad_apps.core.models import Divisao


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nome = models.CharField('Nome', max_length=160)
    username = models.CharField('Registro Funcional', max_length=30, unique=True)
    celular = models.CharField('Celular', max_length=20, blank=True, null=True)
    validado = models.BooleanField('Validado', default=False,
                                   help_text='Campo para verificar se o cadastro do usuário foi validado')
    divisoes = models.ManyToManyField(Divisao, blank=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
