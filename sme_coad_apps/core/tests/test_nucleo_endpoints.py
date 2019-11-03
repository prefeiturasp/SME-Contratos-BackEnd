import pytest
from model_mommy import mommy
from rest_framework import status

from ..models import Nucleo, Servidor

pytestmark = pytest.mark.django_db


@pytest.fixture
def nucleo(fake_user):
    return mommy.make(Nucleo, id=1, sigla='nc1', nome='nucleo teste', chefe=fake_user, suplente_chefe=fake_user)


@pytest.fixture
def servidor(fake_user, nucleo):
    return mommy.make(Servidor, nucleo=nucleo, servidor=fake_user)


def test_url_unaunthorized(client):
    response = client.get('/nucleos/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/nucleos/')
    assert response.status_code == status.HTTP_200_OK


def test_url_lookup(authencticated_client):
    response = authencticated_client.get('/nucleos/lookup/')
    assert response.status_code == status.HTTP_200_OK


def test_url_servidores(authencticated_client, fake_user, nucleo):
    response = authencticated_client.get(f'/nucleos/{nucleo.uuid}/servidores/')
    assert response.status_code == status.HTTP_200_OK


def test_url_limpa_servidores(authencticated_client, fake_user, nucleo):
    response = authencticated_client.delete(f'/nucleos/{nucleo.uuid}/limpa-servidores/')
    assert response.status_code == status.HTTP_200_OK

# TODO Fazer funcionar esse teste
# def test_url_update_servidores(authencticated_client, fake_user, nucleo, servidor):
#     servidor_json = ServidorSerializer(servidor, many=True).data
#     # servidores = [json.dumps(servidor_json), ]
#     response = authencticated_client.post(f'/nucleos/{nucleo.uuid}/update-servidores/',
#     servidor_json, content_type="application/json")
#     assert response.status_code == status.HTTP_200_OK
