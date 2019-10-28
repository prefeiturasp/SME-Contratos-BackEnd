import base64
import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nome = models.CharField('Nome', max_length=160)
    username = models.CharField('Registro Funcional', max_length=30, unique=True)
    celular = models.CharField('Celular', max_length=20, blank=True, default='')
    validado = models.BooleanField('Validado', default=False,
                                   help_text='Campo para verificar se o cadastro do usuário foi validado')
    hash_redefinicao = models.TextField(blank=True, default='',
                                        help_text='Campo utilizado para registrar hash na redefinição de senhas')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def encode_hash(self):
        hash_encode = base64.b64encode(str(self.uuid).encode('utf-8') + str(self.username).encode('utf-8'))
        return hash_encode.decode('utf-8')

    def validar_hash(self, hash_encode):
        if hash_encode == self.encode_hash:
            return True
        return False

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
