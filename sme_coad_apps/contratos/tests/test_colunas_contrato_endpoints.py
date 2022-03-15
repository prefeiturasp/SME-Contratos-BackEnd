import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/colunas-contrato/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(client_autenticado):
    response = client_autenticado.get('/colunas-contrato/')
    assert response.status_code == status.HTTP_200_OK
