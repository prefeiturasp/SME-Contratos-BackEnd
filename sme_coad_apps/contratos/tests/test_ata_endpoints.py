import pytest
from model_mommy import mommy
from rest_framework import status

from ..models.contrato import Edital

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/atas/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/atas/')
    assert response.status_code == status.HTTP_200_OK


def test_url_authorized_por_edital(authencticated_client):
    edital = mommy.make(Edital, id=1, numero='1234/2022')
    response = authencticated_client.get(f'/atas/atas-por-edital/{str(edital.uuid)}/')
    assert response.status_code == status.HTTP_200_OK
