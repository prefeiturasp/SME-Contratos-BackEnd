import datetime
import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/aditamentos/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/aditamentos/')
    assert response.status_code == status.HTTP_200_OK


def test_url_unauthorized_objetos(client):
    response = client.get('/aditamentos/objetos/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized_objetos(authencticated_client):
    response = authencticated_client.get('/aditamentos/objetos/')
    assert response.status_code == status.HTTP_200_OK


def test_post_aditamento_valida_objetos(authencticated_client):
    contrato = mommy.make(
        Contrato,
        termo_contrato='00/00',
        criado_em=datetime.date(2019, 10, 1),
    )
    payload = {
        'contrato': str(contrato.uuid),
        'objeto_aditamento': [
            'MODIFICACAO_VALOR_CONTRATUAL'
        ],
        'termo_aditivo': '00001/2022',
        'razoes_aditamento': 'teste'
    }

    response = authencticated_client.post(
        '/aditamentos/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
