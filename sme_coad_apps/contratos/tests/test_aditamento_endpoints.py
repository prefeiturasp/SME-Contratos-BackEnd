import pytest
from rest_framework import status

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
