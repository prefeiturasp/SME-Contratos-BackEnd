import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import TipoServicoAdmin
from ..models import TipoServico

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make('TipoServico', nome='Limpeza')
    assert isinstance(model, TipoServico)
    assert isinstance(model.nome, str)
    assert model.historico


def test_srt_model():
    model = mommy.make('TipoServico', nome='Limpeza')
    assert model.__str__() == 'Limpeza'


def test_meta_modelo():
    model = mommy.make('TipoServico')
    assert model._meta.verbose_name == 'Tipo de Serviço'
    assert model._meta.verbose_name_plural == 'Tipos de Serviço'


def test_admin():
    model_admin = TipoServicoAdmin(TipoServico, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[TipoServico]
    assert model_admin.list_display == ('nome',)
    assert model_admin.ordering == ('nome',)
    assert model_admin.search_fields == ('nome',)
