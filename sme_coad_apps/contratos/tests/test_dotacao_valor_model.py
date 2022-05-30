import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import DotacaoValorAdmin
from ..models import Contrato, DotacaoValor
from ..models.dotacao_valor import DotacaoOrcamentaria, Empenho

pytestmark = pytest.mark.django_db


def test_instance_model(dotacao_orcamentaria):
    contrato = mommy.make('Contrato')
    dotacao_valor = mommy.make('DotacaoValor', contrato=contrato, dotacao_orcamentaria=dotacao_orcamentaria,
                               valor='2000')
    empenho = mommy.make('Empenho', dotacao_valor=dotacao_valor, numero='123456', valor_previsto=1000)

    assert isinstance(dotacao_valor, DotacaoValor)
    assert isinstance(dotacao_valor.contrato, Contrato)
    assert isinstance(dotacao_valor.dotacao_orcamentaria, DotacaoOrcamentaria)
    assert isinstance(dotacao_valor.valor, str)

    assert isinstance(empenho, Empenho)
    assert isinstance(empenho.dotacao_valor, DotacaoValor)
    assert isinstance(empenho.numero, str)


def test_srt_model(dotacao_orcamentaria):
    contrato = mommy.make('Contrato')
    model = mommy.make('DotacaoValor', contrato=contrato, dotacao_orcamentaria=dotacao_orcamentaria, valor='2000')
    assert model.__str__() == f'{contrato.termo_contrato} - {model.dotacao_orcamentaria} - R${model.valor}'


def test_admin():
    model_admin = DotacaoValorAdmin(DotacaoValor, admin.site)
    assert admin.site._registry[DotacaoValor]
    assert model_admin.list_display == ['contrato', 'dotacao_orcamentaria', 'valor', ]
    assert model_admin.ordering == ('contrato',)
