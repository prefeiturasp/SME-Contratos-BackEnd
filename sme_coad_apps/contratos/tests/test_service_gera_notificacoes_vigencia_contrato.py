import datetime

import pytest
from freezegun import freeze_time
from model_mommy import mommy

from ..models import Contrato, NotificacaoVigenciaContrato
from ..services import gera_notificacoes_vigencia_contratos

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
                      )


@freeze_time('2019-03-12')
def test_gera_notificacao_30_dias(parametro_notificacao, contrato):
    assert not NotificacaoVigenciaContrato.objects.all().exists()
    gera_notificacoes_vigencia_contratos()
    assert NotificacaoVigenciaContrato.objects.all().count() == 1
