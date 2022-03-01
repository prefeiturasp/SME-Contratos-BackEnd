import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import ObrigacaoContratualAdmin
from ..models import Contrato, ObrigacaoContratual

pytestmark = pytest.mark.django_db


def test_instance_model():
    contrato = mommy.make('Contrato')
    obrigacao_contratual = mommy.make('ObrigacaoContratual', contrato=contrato, item='001', obrigacao='Teste')

    assert isinstance(obrigacao_contratual, ObrigacaoContratual)
    assert isinstance(obrigacao_contratual.contrato, Contrato)
    assert isinstance(obrigacao_contratual.item, str)
    assert isinstance(obrigacao_contratual.obrigacao, str)


def test_srt_model():
    contrato = mommy.make('Contrato')
    model = mommy.make('ObrigacaoContratual', contrato=contrato, obrigacao='Teste')
    assert model.__str__() == f'{contrato.termo_contrato} - {model.obrigacao}'


def test_admin():
    model_admin = ObrigacaoContratualAdmin(ObrigacaoContratual, admin.site)
    assert admin.site._registry[ObrigacaoContratual]
    assert model_admin.list_display == ['contrato', 'item', 'obrigacao', ]
    assert model_admin.ordering == ('contrato',)
