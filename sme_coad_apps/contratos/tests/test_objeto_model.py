import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import ObjetoAdmin
from ..models import Objeto

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make('Objeto', nome='Limpeza')
    assert isinstance(model, Objeto)
    assert isinstance(model.nome, str)
    assert model.historico


def test_srt_model():
    model = mommy.make('Objeto', nome='Limpeza')
    assert model.__str__() == 'Limpeza'


def test_meta_modelo():
    model = mommy.make('Objeto')
    assert model._meta.verbose_name == 'Objeto'
    assert model._meta.verbose_name_plural == 'Objetos'


def test_admin():
    model_admin = ObjetoAdmin(Objeto, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Objeto]
    assert model_admin.list_display == ('nome',)
    assert model_admin.ordering == ('nome',)
    assert model_admin.search_fields == ('nome',)
