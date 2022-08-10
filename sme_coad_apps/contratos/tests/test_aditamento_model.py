import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import AditamentoAdmin
from ..models import Aditamento, Contrato

pytestmark = pytest.mark.django_db


def test_instance_model(aditamento):
    assert isinstance(aditamento, Aditamento)
    assert isinstance(aditamento.termo_aditivo, str)
    assert isinstance(aditamento.contrato, Contrato)
    assert isinstance(aditamento.objeto_aditamento, str)
    assert isinstance(aditamento.data_inicial, datetime.date)
    assert isinstance(aditamento.data_final, datetime.date)
    assert isinstance(aditamento.razoes_aditamento, str)
    assert isinstance(aditamento.valor_mensal_atualizado, float)
    assert isinstance(aditamento.valor_total_atualizado, float)
    assert isinstance(aditamento.valor_aditamento, float)


def test_objetos_aditamento():
    assert Aditamento.OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL
    assert Aditamento.OBJETO_MODIFICACAO_PROJETO_ESPECIFICACOES
    assert Aditamento.OBJETO_MODIFICACAO_VALOR_CONTRATUAL
    assert Aditamento.OBJETO_SUBSTITUICAO_GARANTIA_EXECUCAO
    assert Aditamento.OBJETO_MODIFICACAO_REGIME_EXECUCAO
    assert Aditamento.OBJETO_MODIFICACAO_FORMA_PAGAMENTO


def test_srt_model():
    model = mommy.make('Aditamento', termo_aditivo='12345/2022')
    assert model.__str__() == '12345/2022'


def test_meta_modelo():
    model = mommy.make('Aditamento')
    assert model._meta.verbose_name == 'Aditamento'
    assert model._meta.verbose_name_plural == 'Aditamentos'


def test_admin():
    model_admin = AditamentoAdmin(Aditamento, admin.site)
    assert admin.site._registry[Aditamento]
    assert model_admin.list_display == ('termo_aditivo', 'contrato', 'objeto_aditamento', 'data_inicial',
                                        'data_final', 'valor_total_atualizado')
    assert model_admin.search_fields == ('termo_aditivo',)
