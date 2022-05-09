import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import ProdutoAdmin, UnidadeDeMedidaAdmin
from ..models import Produto, UnidadeDeMedida

pytestmark = pytest.mark.django_db


def test_instance_model_unidade_medida():
    model = mommy.make('UnidadeDeMedida', nome='Kilograma')
    assert isinstance(model, UnidadeDeMedida)
    assert isinstance(model.nome, str)


def test_instance_model_produto():
    model = mommy.make('Produto', nome='Produto Teste')
    assert isinstance(model, Produto)
    assert isinstance(model.nome, str)
    assert isinstance(model.categoria, str)
    assert isinstance(model.situacao, str)
    assert isinstance(model.grupo_alimentar, str)
    assert isinstance(model.durabilidade, str)
    assert isinstance(model.armazenabilidade, str)
    assert isinstance(model.unidade_medida, UnidadeDeMedida)
    assert model.historico


def test_srt_model_unidade_medida():
    model = mommy.make('UnidadeDeMedida', nome='litro')
    assert model.__str__() == 'litro'


def test_srt_model_produto():
    model = mommy.make('Produto', nome='Produto Perecível')
    assert model.__str__() == 'PRODUTO PERECÍVEL'


def test_meta_modelo():
    model = mommy.make('Produto')
    assert model._meta.verbose_name == 'Produto'
    assert model._meta.verbose_name_plural == 'Produtos'


def test_admin_unidade_medida():
    model_admin = UnidadeDeMedidaAdmin(UnidadeDeMedida, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[UnidadeDeMedida]
    assert model_admin.list_display == ('nome', 'criado_em')
    assert model_admin.ordering == ('nome',)
    assert model_admin.search_fields == ('nome',)


def test_admin_produto():
    model_admin = ProdutoAdmin(Produto, admin.site)
    assert admin.site._registry[Produto]
    assert model_admin.list_display == (
        'nome',
        'situacao',
        'categoria',
        'grupo_alimentar',
        'unidade_medida',
        'criado_em'
    )
    assert model_admin.ordering == ('nome',)
    assert model_admin.search_fields == ('nome',)
