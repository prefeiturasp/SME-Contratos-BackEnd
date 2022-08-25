import datetime
import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/intercorrencias/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/intercorrencias/')
    assert response.status_code == status.HTTP_200_OK


def test_url_unauthorized_objetos(client):
    response = client.get('/intercorrencias/motivos-suspensao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized_objetos(authencticated_client):
    response = authencticated_client.get('/intercorrencias/motivos-suspensao/')
    assert response.status_code == status.HTTP_200_OK


def test_post_intercorrencia_valida_objetos(authencticated_client):
    contrato = mommy.make(
        Contrato,
        termo_contrato='00/00',
        criado_em=datetime.date(2019, 10, 1),
    )
    payload = {
        'contrato': str(contrato.uuid),
        'tipo_intercorrencia': 'SUSPENSAO',
        'data_inicial': '2022-08-26',
        'data_final': '2022-09-20',
        'acrescentar_dias': True,
        'motivo_suspensao': 'UNILATERALMENTE_ADMINISTRACAO_PUBLICA',
        'opcao_suspensao': 'Conveniência da Administração Pública',
        'descricao_suspensao': 'Teste de descrição de post'
    }

    response = authencticated_client.post(
        '/intercorrencias/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED
