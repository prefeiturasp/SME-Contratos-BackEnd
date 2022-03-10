import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import EditalAdmin
from ..models import Edital, TipoServico

pytestmark = pytest.mark.django_db

def test_instance_model(edital):
    assert isinstance(edital, Edital)
    assert isinstance(edital.numero, str)
    assert isinstance(edital.processo, str)
    assert isinstance(edital.tipo_contratacao, str)
    assert isinstance(edital.subtipo, str)
    assert isinstance(edital.status, str)
    assert isinstance(edital.data_homologacao, datetime.date)
    assert isinstance(edital.objeto, TipoServico)
    assert isinstance(edital.descricao_objeto, str)
    assert edital.historico


def test_status():
    assert Edital.ATIVO
    assert Edital.INATIVO


def test_tipo_contratacao():
    assert Edital.TIPO_LICITACAO
    assert Edital.TIPO_DISPENSA_LICITACAO
    assert Edital.TIPO_INEXIGIBILIDADE_LICITACAO


def test_srt_model():
    model = mommy.make('Edital', numero='0123456')
    assert model.__str__() == '0123456'


def test_meta_modelo():
    model = mommy.make('Edital')
    assert model._meta.verbose_name == 'Edital'
    assert model._meta.verbose_name_plural == 'Editais'


def test_admin():
    model_admin = EditalAdmin(Edital, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Edital]
    assert model_admin.list_display == ('numero',)
    assert model_admin.ordering == ('numero',)
    assert model_admin.search_fields == ('numero',)
