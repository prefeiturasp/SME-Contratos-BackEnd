import json

import pytest
from model_mommy import mommy
from rest_framework import status

from sme_coad_apps.contratos.models import Produto, UnidadeDeMedida

pytestmark = pytest.mark.django_db


def test_url_unauthorized_unidades_medida(client):
    response = client.get('/unidades-de-medida/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized_unidades_medida(authencticated_client):
    response = authencticated_client.get('/unidades-de-medida/')
    assert response.status_code == status.HTTP_200_OK


def test_url_unauthorized_produtos(client):
    response = client.get('/produtos/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized_produtos(authencticated_client):
    response = authencticated_client.get('/produtos/')
    assert response.status_code == status.HTTP_200_OK


def test_url_authorized_produtos_simples(authencticated_client):
    response = authencticated_client.get('/produtos/simples/')
    assert response.status_code == status.HTTP_200_OK


def test_post_produto(authencticated_client):
    unidade_medida = mommy.make(UnidadeDeMedida, id=1, nome='ARROZ')
    payload = {
        'unidade_medida': str(unidade_medida.uuid),
        'nome': 'Produto Teste',
        'categoria': Produto.CATEGORIA_ALIMENTO,
        'situacao': Produto.SITUACAO_ATIVO,
        'grupo_alimentar': Produto.GRUPO_ALIMENTAR_SECOS,
        'tipo_programa': Produto.TIPO_PROGRAMA_LEVE_LEITE
    }

    response = authencticated_client.post(
        '/produtos/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED
