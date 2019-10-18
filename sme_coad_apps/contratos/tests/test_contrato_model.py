import datetime

import pytest
from django.contrib import admin
from freezegun import freeze_time
from model_mommy import mommy

from ..admin import ContratoAdmin
from ..models import Contrato, ContratoUnidade, TipoServico, Empresa
from ...core.models import Nucleo, Unidade
from ...users.models import User

# from ..admin import TipoServicoAdmin

pytestmark = pytest.mark.django_db


def test_instance_model():
    gestor = mommy.make(User)
    model = mommy.make('Contrato', data_assinatura=datetime.date(2019, 1, 1),
                       data_ordem_inicio=datetime.date(2019, 1, 1), vigencia_em_dias=100, gestor=gestor,
                       observacoes='teste')
    assert isinstance(model, Contrato)
    assert isinstance(model.termo_contrato, str)
    assert isinstance(model.processo, str)
    assert isinstance(model.tipo_servico, TipoServico)
    assert isinstance(model.nucleo_responsavel, Nucleo)
    assert isinstance(model.objeto, str)
    assert isinstance(model.empresa_contratada, Empresa)
    assert isinstance(model.data_assinatura, datetime.date)
    assert isinstance(model.data_ordem_inicio, datetime.date)
    assert isinstance(model.vigencia_em_dias, int)
    assert isinstance(model.situacao, str)
    assert isinstance(model.gestor, User)
    assert isinstance(model.observacoes, str)
    assert isinstance(model.estado_contrato, str)
    assert isinstance(model.data_encerramento, datetime.date)
    assert model.historico


def test_srt_model():
    tipo_servico = mommy.make(TipoServico, nome='teste')
    model = mommy.make('Contrato', termo_contrato='XPTO123', tipo_servico=tipo_servico,
                       situacao=Contrato.SITUACAO_ATIVO)
    assert model.__str__() == f'TC:XPTO123 - teste - {Contrato.SITUACAO_NOMES[Contrato.SITUACAO_ATIVO]}'


def test_meta_modelo():
    model = mommy.make('Contrato')
    assert model._meta.verbose_name == 'Contrato'
    assert model._meta.verbose_name_plural == 'Contratos'


def test_field_data_encerramento():
    model = mommy.make('Contrato', data_ordem_inicio=datetime.date(2018, 12, 1), vigencia_em_dias=30)
    assert model.data_encerramento == datetime.date(2018, 12, 31)


@freeze_time('2018-12-15')
def test_property_dias_para_o_encerramento():
    model = mommy.make('Contrato', data_ordem_inicio=datetime.date(2018, 12, 1), vigencia_em_dias=30)
    assert model.dias_para_o_encerramento == 16


def test_property_total_mensal():
    contrato = mommy.make('Contrato')
    unidade1 = mommy.make('Unidade', codigo_eol='123456')
    unidade2 = mommy.make('Unidade', codigo_eol='789012')
    mommy.make('ContratoUnidade', contrato=contrato, lote='1', unidade=unidade1, valor_mensal=100)
    mommy.make('ContratoUnidade', contrato=contrato, lote='1', unidade=unidade2, valor_mensal=200)
    assert contrato.total_mensal == 300


def test_instance_model_detalhe():
    contrato = mommy.make('Contrato')
    unidade = mommy.make('Unidade', codigo_eol='123456')
    model = mommy.make('ContratoUnidade', contrato=contrato, lote='1', unidade=unidade)
    assert isinstance(model, ContratoUnidade)
    assert isinstance(model.contrato, Contrato)
    assert isinstance(model.unidade, Unidade)
    assert isinstance(model.valor_mensal, float)
    assert isinstance(model.valor_total, float)
    assert isinstance(model.dotacao_orcamentaria, str)
    assert isinstance(model.lote, str)
    assert model.historico


def test_srt_model_detalhe():
    unidade = mommy.make(Unidade, nome='Teste', codigo_eol='123456')
    contrato = mommy.make('Contrato', termo_contrato='XPTO123')
    model = mommy.make('ContratoUnidade', contrato=contrato, unidade=unidade)
    assert model.__str__() == f'TC:XPTO123 - Unidade: Teste'


def test_admin():
    model_admin = ContratoAdmin(Contrato, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Contrato]
    assert model_admin.list_display == (
        'termo_contrato',
        'processo',
        'tipo_servico',
        'empresa_contratada',
        'valor_mensal',
        'data_inicio',
        'data_fim',
        'dias_para_vencer',
        'estado_contrato',
        'situacao'
    )
    assert model_admin.ordering == ('termo_contrato',)
    assert model_admin.search_fields == ('processo', 'termo_contrato')
    assert model_admin.list_filter == ('tipo_servico', 'empresa_contratada', 'situacao', 'estado_contrato')
