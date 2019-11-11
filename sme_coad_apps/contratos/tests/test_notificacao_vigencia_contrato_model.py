import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import NotificacaoVigenciaContratoAdmin
from ..models import NotificacaoVigenciaContrato, Contrato
from ...users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def contrato(gestor, suplente):
    return mommy.make('Contrato', data_assinatura=datetime.date(2019, 1, 1),
                      data_ordem_inicio=datetime.date(2019, 1, 1), vigencia_em_dias=100, gestor=gestor,
                      suplente=suplente, estado_contrato=Contrato.ESTADO_EMERGENCIAL,
                      termo_contrato='999/99',
                      )


@pytest.fixture
def notificacao_vigencia_contrato(contrato, gestor):
    return mommy.make(
        'NotificacaoVigenciaContrato',
        contrato=contrato,
        notificado=gestor,
        validade=datetime.datetime(2019, 1, 1)
    )


def test_instance_model(notificacao_vigencia_contrato):
    assert isinstance(notificacao_vigencia_contrato, NotificacaoVigenciaContrato)
    assert isinstance(notificacao_vigencia_contrato.contrato, Contrato)
    assert isinstance(notificacao_vigencia_contrato.notificado, User)
    assert isinstance(notificacao_vigencia_contrato.validade, datetime.date)
    assert notificacao_vigencia_contrato.uuid


def test_srt_model(notificacao_vigencia_contrato):
    expected = f"TC:{notificacao_vigencia_contrato.contrato.termo_contrato} " \
               f"Notificado:{notificacao_vigencia_contrato.notificado.username} " \
               f"Validade:{notificacao_vigencia_contrato.validade}"
    assert notificacao_vigencia_contrato.__str__() == expected


def test_meta_modelo(notificacao_vigencia_contrato):
    assert notificacao_vigencia_contrato._meta.verbose_name == 'Notificação de vigência de contrato'
    assert notificacao_vigencia_contrato._meta.verbose_name_plural == 'Notificações de vigência de contrato'


def test_admin():
    model_admin = NotificacaoVigenciaContratoAdmin(NotificacaoVigenciaContrato, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[NotificacaoVigenciaContrato]
    assert model_admin.list_display == ('criado_em', 'termo_contrato', 'notificado', 'validade')
    assert model_admin.ordering == ('criado_em', 'contrato', 'notificado')
    assert model_admin.list_filter == ('notificado',)
