import datetime

import pytest
from django.contrib import admin
from freezegun import freeze_time
from model_mommy import mommy

from ..admin import ContratoAdmin
from ..models import Contrato, ContratoUnidade, TipoServico, Empresa
from ...atestes.models import ModeloAteste
from ...core.models import Nucleo, Unidade, Edital
from ...users.models import User

# from ..admin import TipoServicoAdmin

pytestmark = pytest.mark.django_db


@pytest.fixture
def gestor():
    return mommy.make(User)


@pytest.fixture
def suplente():
    return mommy.make(User)


@pytest.fixture
def contrato_emergencial(gestor, suplente):
    return mommy.make('Contrato', data_assinatura=datetime.date(2019, 1, 1),
                      data_ordem_inicio=datetime.date(2019, 1, 1), vigencia_em_dias=100, gestor=gestor,
                      suplente=suplente, observacoes='teste', tipo_servico=mommy.make(TipoServico),
                      nucleo_responsavel=mommy.make(Nucleo), edital=mommy.make(Edital), empresa_contratada=mommy.make(Empresa),
                      estado_contrato=Contrato.ESTADO_EMERGENCIAL, modelo_ateste=mommy.make(ModeloAteste)
                      )


@pytest.fixture
def dre_aa():
    return 'DRE - SA'


@pytest.fixture
def dre_bb():
    return 'DRE - JT'


@pytest.fixture
def unidade_123456(dre_aa):
    return mommy.make(Unidade, nome='Teste', codigo_eol='123456', dre=dre_aa)


@pytest.fixture
def unidade_654321(dre_bb):
    return mommy.make(Unidade, nome='Teste', codigo_eol='654321', dre=dre_bb)


@pytest.fixture
def contrato_xpto123():
    return mommy.make('Contrato', termo_contrato='XPTO123')


@pytest.fixture
def contrato_unidade_xpto123_123456(contrato_xpto123, unidade_123456):
    lote = mommy.make('Lote', nome='1', contrato=contrato_xpto123)
    lote.unidades.add(unidade_123456)
    return mommy.make('ContratoUnidade', contrato=contrato_xpto123, unidade=unidade_123456)


@pytest.fixture
def contrato_unidade_xpto123_654321(contrato_xpto123, unidade_654321):
    lote = mommy.make('Lote', nome='2', contrato=contrato_xpto123)
    lote.unidades.add(unidade_654321)
    return mommy.make('ContratoUnidade', contrato=contrato_xpto123, unidade=unidade_654321)


def test_instance_model(contrato_emergencial):
    assert isinstance(contrato_emergencial.termo_contrato, str)
    assert isinstance(contrato_emergencial, Contrato)
    assert isinstance(contrato_emergencial.processo, str)
    assert isinstance(contrato_emergencial.tipo_servico, TipoServico)
    assert isinstance(contrato_emergencial.nucleo_responsavel, Nucleo)
    assert isinstance(contrato_emergencial.edital, Edital)
    assert isinstance(contrato_emergencial.objeto, str)
    assert isinstance(contrato_emergencial.empresa_contratada, Empresa)
    assert isinstance(contrato_emergencial.data_assinatura, datetime.date)
    assert isinstance(contrato_emergencial.data_ordem_inicio, datetime.date)
    assert isinstance(contrato_emergencial.referencia_encerramento, str)
    assert isinstance(contrato_emergencial.vigencia_em_dias, int)
    assert isinstance(contrato_emergencial.situacao, str)
    assert isinstance(contrato_emergencial.gestor, User)
    assert isinstance(contrato_emergencial.suplente, User)
    assert isinstance(contrato_emergencial.observacoes, str)
    assert isinstance(contrato_emergencial.estado_contrato, str)
    assert isinstance(contrato_emergencial.data_encerramento, datetime.date)
    assert isinstance(contrato_emergencial.valor_total, float)
    assert contrato_emergencial.historico
    assert isinstance(contrato_emergencial.modelo_ateste, ModeloAteste)
    assert contrato_emergencial.dres == ""


def test_srt_model():
    tipo_servico = mommy.make(TipoServico, nome='teste')
    model = mommy.make('Contrato', termo_contrato='XPTO123', tipo_servico=tipo_servico,
                       situacao=Contrato.SITUACAO_ATIVO)
    assert model.__str__() == 'XPTO123'


def test_meta_modelo():
    model = mommy.make('Contrato')
    assert model._meta.verbose_name == 'Contrato'
    assert model._meta.verbose_name_plural == 'Contratos'


def test_situcoes():
    assert Contrato.SITUACAO_ATIVO
    assert Contrato.SITUACAO_ENCERRADO
    assert Contrato.SITUACAO_RASCUNHO


def test_estado():
    assert Contrato.ESTADO_EMERGENCIAL
    assert Contrato.ESTADO_EXCEPCIONAL
    assert Contrato.ESTADO_SUSPENSO_INTERROMPIDO
    assert Contrato.ESTADO_VIGENTE


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


def test_instance_model_detalhe(contrato_xpto123, unidade_123456):
    model = mommy.make('ContratoUnidade', contrato=contrato_xpto123, lote='1', unidade=unidade_123456)
    assert isinstance(model.contrato, Contrato)
    assert isinstance(model, ContratoUnidade)
    assert isinstance(model.unidade, Unidade)
    assert isinstance(model.valor_mensal, float)
    assert isinstance(model.valor_total, float)
    assert isinstance(model.lote, str)
    assert model.historico


def test_srt_model_detalhe(contrato_xpto123, unidade_123456):
    model = mommy.make('ContratoUnidade', contrato=contrato_xpto123, unidade=unidade_123456)
    assert model.__str__() == f'TC:XPTO123 - Unidade: Teste'


def test_admin():
    model_admin = ContratoAdmin(Contrato, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Contrato]
    assert model_admin.list_display == (
        'termo_contrato',
        'tipo_servico',
        'empresa_contratada',
        'dres',
        'data_inicio',
        'data_fim',
        'dias_para_vencer',
        'estado_contrato',
        'situacao'
    )
    assert model_admin.ordering == ('termo_contrato',)
    assert model_admin.search_fields == ('processo', 'termo_contrato')
    assert model_admin.list_filter == ('tipo_servico', 'empresa_contratada', 'situacao', 'estado_contrato')


def test_contratos_no_estado():
    mommy.make(Contrato, estado_contrato=Contrato.ESTADO_EXCEPCIONAL, _quantity=3)
    mommy.make(Contrato, estado_contrato=Contrato.ESTADO_VIGENTE, _quantity=2)
    assert Contrato.contratos_no_estado(Contrato.ESTADO_EXCEPCIONAL).count() == 3


def test_contratos_no_estado_vencendo_ate():
    mommy.make(Contrato, estado_contrato=Contrato.ESTADO_EXCEPCIONAL, data_encerramento="2020-01-01", _quantity=3)
    mommy.make(Contrato, estado_contrato=Contrato.ESTADO_EXCEPCIONAL, data_encerramento="2021-01-01", _quantity=2)
    mommy.make(Contrato, estado_contrato=Contrato.ESTADO_VIGENTE, data_encerramento="2020-01-01", _quantity=2)

    assert Contrato.contratos_no_estado(Contrato.ESTADO_EXCEPCIONAL, vencendo_ate="2020-02-01").count() == 3


def test_notifica_atribuicao(contrato_emergencial):
    notificacoes_gestor = contrato_emergencial.gestor \
        .notifications.unread().filter(verb='tc_atribuido_gestor', actor_object_id=contrato_emergencial.id)

    notificacoes_suplente = contrato_emergencial.suplente \
        .notifications.unread().filter(verb='tc_atribuido_suplente', actor_object_id=contrato_emergencial.id)

    assert notificacoes_gestor.exists()
    assert notificacoes_suplente.exists()


def test_dres_do_contrato(contrato_unidade_xpto123_123456, contrato_unidade_xpto123_654321):
    contrato = contrato_unidade_xpto123_123456.contrato
    assert contrato.dres == 'DRE - JT, DRE - SA'
