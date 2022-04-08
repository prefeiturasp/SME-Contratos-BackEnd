import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import AtaAdmin
from ..models import Ata, Edital

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
