import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/tipos-servico/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/tipos-servico/')
    assert response.status_code == status.HTTP_200_OK


def test_url_lookup(authencticated_client):
    response = authencticated_client.get('/tipos-servico/lookup/')
    assert response.status_code == status.HTTP_200_OK


def test_url_created(authencticated_client):
    data = {'nome': 'TestApi'}
    response = authencticated_client.post('/tipos-servico/', data, format='json')
    response_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_json.get('nome') == 'TESTAPI'
