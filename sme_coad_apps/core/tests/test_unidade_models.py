import pytest
from django.contrib import admin
from model_mommy import mommy

from ..models import Unidade
from ..admin import UnidadeAdmin

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make(Unidade, codigo_eol='123456', cep='27600-000')
    assert isinstance(model, Unidade)
    assert isinstance(model.nome, str)
    assert isinstance(model.equipamento, str)
    assert isinstance(model.tipo_unidade, str)
    assert isinstance(model.codigo_eol, str)
    assert isinstance(model.cep, str)


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
    assert model_admin.list_display == ('equipamento', 'nome', 'tipo_unidade', 'codigo_eol')
    assert model_admin.ordering == ('equipamento', 'nome', 'tipo_unidade', 'codigo_eol')
    assert model_admin.search_fields == ('nome', 'codigo_eol')
    assert model_admin.list_filter == ('equipamento', 'tipo_unidade')
