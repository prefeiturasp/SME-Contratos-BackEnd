import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import ColunasContratoAdmin
from ..models import ColunasContrato
from ...users.models import User

pytestmark = pytest.mark.django_db


def test_instance_model():
    usuario = mommy.make(User)
    array_campos = ['teste1', 'teste2']
    model = mommy.make('ColunasContrato', usuario=usuario, colunas_array=array_campos)
    assert isinstance(model, ColunasContrato)
    assert isinstance(model.usuario, User)


def test_srt_model():
    usuario = mommy.make(User)
    model = mommy.make('ColunasContrato', usuario=usuario)
    assert model.__str__() == usuario.nome


def test_meta_modelo():
    model = mommy.make('ColunasContrato')
    assert model._meta.verbose_name == 'Colunas do Usuário'
    assert model._meta.verbose_name_plural == 'Colunas do Usuário'


def test_admin():
    model_admin = ColunasContratoAdmin(ColunasContrato, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[ColunasContrato]
    assert model_admin.list_display == ('usuario', 'colunas_array',)
    assert model_admin.ordering == ('usuario',)
    assert model_admin.search_fields == ('usuario',)
