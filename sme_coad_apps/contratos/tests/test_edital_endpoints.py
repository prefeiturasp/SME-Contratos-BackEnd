import json

import pytest
from rest_framework import status

from ..models.edital import Edital

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/editais/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/editais/')
    assert response.status_code == status.HTTP_200_OK


def test_url_tipo_contratacao(authencticated_client):
    response = authencticated_client.get('/editais/tipo_contratacao/')
    assert response.status_code == status.HTTP_200_OK
    json_data = json.loads(response.content)
    assert json_data == Edital.tipo_contratacao_to_json()
