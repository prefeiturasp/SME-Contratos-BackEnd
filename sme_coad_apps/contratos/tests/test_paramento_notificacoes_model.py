import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import ParametroNotificacoesVigenciaAdmin
from ..models import ParametroNotificacoesVigencia, Contrato

pytestmark = pytest.mark.django_db


@pytest.fixture
def parametro_notificacao():
    return mommy.make(
        'ParametroNotificacoesVigencia',
        estado_contrato=Contrato.ESTADO_EMERGENCIAL,
        vencendo_em=100,
        repetir_notificacao_a_cada=7,
    )


def test_instance_model(parametro_notificacao):
    assert isinstance(parametro_notificacao, ParametroNotificacoesVigencia)
    assert isinstance(parametro_notificacao.estado_contrato, str)
    assert isinstance(parametro_notificacao.vencendo_em, int)
    assert isinstance(parametro_notificacao.repetir_notificacao_a_cada, int)
    assert parametro_notificacao.historico


def test_srt_model(parametro_notificacao):
    expected = f"Contratos {Contrato.ESTADO_NOMES[parametro_notificacao.estado_contrato]} " \
               f"notificar a partir de {parametro_notificacao.vencendo_em} dias " \
               f"repetindo a cada {parametro_notificacao.repetir_notificacao_a_cada} dias."
    assert parametro_notificacao.__str__() == expected


def test_meta_modelo(parametro_notificacao):
    assert parametro_notificacao._meta.verbose_name == 'Parâmetro de notificação de vigência'
    assert parametro_notificacao._meta.verbose_name_plural == 'Parâmetros de notificação de vigência'


def test_admin():
    model_admin = ParametroNotificacoesVigenciaAdmin(ParametroNotificacoesVigencia, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[ParametroNotificacoesVigencia]
    assert model_admin.list_display == ('estado_contrato', 'vencendo_em', 'repetir_notificacao_a_cada')
    assert model_admin.ordering == ('estado_contrato',)
    assert model_admin.list_filter == ('estado_contrato',)
