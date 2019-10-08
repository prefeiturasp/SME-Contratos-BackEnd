import json

import pytest
from rest_framework import status

from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/contratos/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/contratos/')
    assert response.status_code == status.HTTP_200_OK


def test_url_estados(authencticated_client):
    response = authencticated_client.get('/contratos/estados/')
    assert response.status_code == status.HTTP_200_OK
    json_data = json.loads(response.content)
    assert json_data == Contrato.estados_to_json()
