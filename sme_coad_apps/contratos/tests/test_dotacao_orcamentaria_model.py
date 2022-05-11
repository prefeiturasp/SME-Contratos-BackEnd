import pytest
from django.contrib import admin

from ..admin import DotacaoOrcamentariaAdmin
from ..models.dotacao_valor import DotacaoOrcamentaria

pytestmark = pytest.mark.django_db


def test_instance_model(dotacao_orcamentaria):

    assert isinstance(dotacao_orcamentaria, DotacaoOrcamentaria)
    assert isinstance(dotacao_orcamentaria.orgao, str)
    assert isinstance(dotacao_orcamentaria.unidade, str)
    assert isinstance(dotacao_orcamentaria.funcao, str)
    assert isinstance(dotacao_orcamentaria.subfuncao, str)
    assert isinstance(dotacao_orcamentaria.programa, str)
    assert isinstance(dotacao_orcamentaria.projeto_atividade, str)
    assert isinstance(dotacao_orcamentaria.conta_despesa, str)
    assert isinstance(dotacao_orcamentaria.fonte, str)


def test_srt_model(dotacao_orcamentaria):
    assert dotacao_orcamentaria.__str__() == f"""{dotacao_orcamentaria.orgao}.
                                                 {dotacao_orcamentaria.unidade}.
                                                 {dotacao_orcamentaria.funcao}.
                                                 {dotacao_orcamentaria.subfuncao}.
                                                 {dotacao_orcamentaria.programa}.
                                                 {dotacao_orcamentaria.projeto_atividade}.
                                                 {dotacao_orcamentaria.conta_despesa}.
                                                 {dotacao_orcamentaria.fonte}"""


def test_admin():
    model_admin = DotacaoOrcamentariaAdmin(DotacaoOrcamentaria, admin.site)
    assert admin.site._registry[DotacaoOrcamentaria]
    assert model_admin.list_display == ['numero_dotacao']
    assert model_admin.ordering == ('orgao',)
