import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/empresas/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/empresas/')
    assert response.status_code == status.HTTP_200_OK


def test_url_lookup(authencticated_client):
    response = authencticated_client.get('/empresas/lookup/')
    assert response.status_code == status.HTTP_200_OK
