import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_url_unauthorizade(client):
    response = client.get('/divisao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authorizade_client):
    response = authorizade_client.get('/divisao/')
    assert response.status_code == status.HTTP_200_OK
