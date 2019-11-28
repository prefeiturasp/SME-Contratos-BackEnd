import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import UnidadeAdmin
from ..models import Unidade

pytestmark = pytest.mark.django_db


@pytest.fixture
def dre():
    return mommy.make(Unidade, codigo_eol='99999', tipo_unidade='DRE')


def test_instance_model(dre):
    model = mommy.make(Unidade, codigo_eol='123456', cep='27600-000', dre=dre)
    assert isinstance(model, Unidade)
    assert isinstance(model.nome, str)
    assert isinstance(model.equipamento, str)
    assert isinstance(model.tipo_unidade, str)
    assert isinstance(model.codigo_eol, str)
    assert isinstance(model.cep, str)
    assert isinstance(model.dre, Unidade)
    assert model.historico


def test_srt_model():
    model = mommy.make(Unidade, nome='Escola Teste')
    assert model.__str__() == 'Escola Teste'


def test_meta_modelo():
    model = mommy.make(Unidade)
    assert model._meta.verbose_name == 'Unidade'
    assert model._meta.verbose_name_plural == 'Unidades'


def test_admin():
    model_admin = UnidadeAdmin(Unidade, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Unidade]
    assert model_admin.list_display == ('nome', 'equipamento', 'tipo_unidade', 'codigo_eol', 'dre')
    assert model_admin.ordering == ('nome',)
    assert model_admin.search_fields == ('nome', 'codigo_eol')
    assert model_admin.list_filter == ('equipamento', 'tipo_unidade', 'dre')
