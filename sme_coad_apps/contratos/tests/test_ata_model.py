import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import AtaAdmin, ProdutosAtaAdmin
from ..models import Ata, Edital, Produto
from ..models.ata import ProdutosAta

pytestmark = pytest.mark.django_db


def test_instance_model(ata):
    assert isinstance(ata, Ata)
    assert isinstance(ata.numero, str)
    assert isinstance(ata.edital, Edital)
    assert isinstance(ata.vigencia, int)
    assert isinstance(ata.unidade_vigencia, str)
    assert isinstance(ata.status, str)
    assert isinstance(ata.data_assinatura, datetime.date)
    assert isinstance(ata.data_encerramento, datetime.date)
    assert ata.historico


def test_status():
    assert Ata.ATIVA
    assert Ata.RASCUNHO
    assert Ata.ENCERRADA


def test_unidade_vigencia():
    assert Ata.UNIDADE_VIGENCIA_DIAS
    assert Ata.UNIDADE_VIGENCIA_MESES


def test_srt_model():
    model = mommy.make('Ata', numero='0123456')
    assert model.__str__() == '0123456'


def test_meta_modelo():
    model = mommy.make('Ata')
    assert model._meta.verbose_name == 'Ata'
    assert model._meta.verbose_name_plural == 'Atas'


def test_admin():
    model_admin = AtaAdmin(Ata, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Ata]
    assert model_admin.list_display == ('numero', 'status', 'empresa', 'data_assinatura', 'data_encerramento')
    assert model_admin.search_fields == ('numero',)


def test_instance_model_produtos_ata(produtos_ata):
    assert isinstance(produtos_ata, ProdutosAta)
    assert isinstance(produtos_ata.ata, Ata)
    assert isinstance(produtos_ata.produto, Produto)
    assert isinstance(produtos_ata.quantidade_total, float)
    assert isinstance(produtos_ata.valor_unitario, float)
    assert isinstance(produtos_ata.valor_total, float)
    assert produtos_ata.historico


def test_srt_model_produtos_ata(ata, produto):
    model = mommy.make('ProdutosAta', ata=ata, produto=produto)
    assert model.__str__() == f'{produto.nome} - {ata.numero}'


def test_meta_modelo_produtos_atas():
    model = mommy.make('ProdutosAta')
    assert model._meta.verbose_name == 'Produto de Ata'
    assert model._meta.verbose_name_plural == 'Produtos de Atas'


def test_admin_produtos_atas():
    model_admin = ProdutosAtaAdmin(ProdutosAta, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[ProdutosAta]
    assert model_admin.list_display == ('ata', 'produto', 'quantidade_total', 'valor_unitario', 'valor_total')
    assert model_admin.search_fields == ('ata',)
