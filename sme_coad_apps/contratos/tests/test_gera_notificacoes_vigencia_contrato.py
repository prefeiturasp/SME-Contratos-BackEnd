import datetime

import pytest
from freezegun import freeze_time
from model_mommy import mommy
from notifications.models import Notification

from ..models import Contrato, NotificacaoVigenciaContrato

pytestmark = pytest.mark.django_db


@pytest.fixture
def parametro_notificacao():
    return mommy.make(
        'ParametroNotificacoesVigencia',
        estado_contrato=Contrato.ESTADO_EMERGENCIAL,
        vencendo_em=30,
        repetir_notificacao_a_cada=7,
    )


@pytest.fixture
def contrato(gestor, suplente):
    return mommy.make('Contrato', data_assinatura=datetime.date(2019, 1, 1),
                      data_ordem_inicio=datetime.date(2019, 1, 1), vigencia_em_dias=100, gestor=gestor,
                      suplente=suplente, estado_contrato=Contrato.ESTADO_EMERGENCIAL,
                      data_encerramento=datetime.date(2019, 4, 11)
                      )


@freeze_time('2019-03-12')
def test_gera_notificacao_30_dias(parametro_notificacao, contrato):
    assert not NotificacaoVigenciaContrato.objects.all().exists()

    NotificacaoVigenciaContrato.gera_notificacoes()
    assert NotificacaoVigenciaContrato.objects.all().count() == 1


@pytest.fixture
@freeze_time('2019-03-12')
def notificacao_30_dias_em_2019_3_12(contrato):
    return mommy.make(
        NotificacaoVigenciaContrato,
        contrato=contrato,
        notificado=contrato.gestor,
    )


@freeze_time('2019-03-19')
def test_gera_notificacao_30_dias_repete_apos_7_dias(parametro_notificacao, contrato, notificacao_30_dias_em_2019_3_12):
    assert NotificacaoVigenciaContrato.objects.all().count() == 1

    assert notificacao_30_dias_em_2019_3_12.idade == 7

    NotificacaoVigenciaContrato.gera_notificacoes()

    assert NotificacaoVigenciaContrato.objects.all().count() == 1


@freeze_time('2019-03-18')
def test_gera_notificacao_30_dias_nao_repete_ates_7_dias(parametro_notificacao, contrato,
                                                         notificacao_30_dias_em_2019_3_12):
    assert NotificacaoVigenciaContrato.objects.all().count() == 1

    assert notificacao_30_dias_em_2019_3_12.idade == 6

    NotificacaoVigenciaContrato.gera_notificacoes()

    assert NotificacaoVigenciaContrato.objects.all().count() == 1


@freeze_time('2019-03-12')
def test_gera_django_notification(parametro_notificacao, contrato):
    NotificacaoVigenciaContrato.gera_notificacoes()
    assert NotificacaoVigenciaContrato.objects.all().count() == 1
    assert Notification.objects.unread().count() == 1

    notificacao = Notification.objects.unread().first()
    assert notificacao.verb == 'alerta_vigencia_contrato'
    assert notificacao.recipient == contrato.gestor
    assert notificacao.description == f'O contrato {contrato.termo_contrato} ' \
        f'está a {contrato.dias_para_o_encerramento} de seu encerramento.'
    assert notificacao.target == contrato
    assert notificacao.target_object_id == f'{contrato.id}'


def test_get_notificacoes_videncia_do_usuario(parametro_notificacao, contrato):
    NotificacaoVigenciaContrato.gera_notificacoes()

    notificacoes = NotificacaoVigenciaContrato.get_notificacoes_do_usuario(usuario=contrato.gestor)

    assert notificacoes.count() == 1
