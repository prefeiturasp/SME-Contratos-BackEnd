import pytest
from faker import Faker
from rest_framework import status

pytestmark = pytest.mark.django_db

url = '/api-token-auth/'
username = Faker().user_name()
password = Faker().text()


def test_redirect(client):
    response = client.get('/usuarios/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_redirect_authenticated(authencticated_client):
    response = authencticated_client.get('/usuarios/')
    assert response.status_code == status.HTTP_200_OK


def test_login_jwt(client, django_user_model):
    u = django_user_model.objects.create_user(username=username, password=password)
    u.is_active = False
    u.save()

    response = client.post(url, {'username': username, 'password': password}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    u.is_active = True
    u.save()

    response = client.post(url, {'username': username, 'password': password}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data


def test_url_lookup(authencticated_client):
    response = authencticated_client.get('/usuarios/lookup/')
    assert response.status_code == status.HTTP_200_OK
