import uuid as uuid

from django.db import models


class Descritivel(models.Model):
    descricao = models.TextField('Descrição', blank=True, null=True)

    class Meta:
        abstract = True


class TemNome(models.Model):
    nome = models.CharField('Nome', max_length=160)

    class Meta:
        abstract = True


class TemAtivo(models.Model):
    ativo = models.BooleanField("Está ativo?", default=True)

    class Meta:
        abstract = True


class TemCriadoEm(models.Model):
    criado_em = models.DateTimeField("Criado em", editable=False, auto_now_add=True)

    class Meta:
        abstract = True


class TemAlteradoEm(models.Model):
    alterado_em = models.DateTimeField("Alterado em", editable=False, auto_now=True)

    class Meta:
        abstract = True


class TemChaveExterna(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class ModeloBase(TemChaveExterna, TemCriadoEm, TemAlteradoEm):
    class Meta:
        abstract = True
