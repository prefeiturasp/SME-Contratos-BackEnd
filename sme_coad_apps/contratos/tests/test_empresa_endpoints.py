import json

import pytest
from rest_framework import status

from sme_coad_apps.contratos.models import Empresa

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


def test_post_empresa(authencticated_client):
    payload = {
        'contatos': [
            {
                'nome': 'Empresa teste',
                'email': 'user@example.com',
                'telefone': '11999999999',
                'cargo': 'Gerente'
            }
        ],
        'nome': 'Empresa teste',
        'cnpj': '21256564000160',
        'razao_social': 'Empresa Teste LTDA',
        'tipo_servico': Empresa.FORNECEDOR,
        'tipo_fornecedor': Empresa.CONVENCIONAL,
        'situacao': Empresa.SITUACAO_ATIVA,
        'cep': '04284000',
        'endereco': 'Rua América',
        'bairro': 'Vila Moinho',
        'cidade': 'São Paulo',
        'estado': 'São Paulo',
        'numero': '100',
        'complemento': ''
    }

    response = authencticated_client.post(
        '/empresas/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_post_empresa_valida_tipo_fornecimento(authencticated_client):
    payload = {
        'contatos': [
            {
                'nome': 'Empresa teste',
                'email': 'user@example.com',
                'telefone': '11999999999',
                'cargo': 'Gerente'
            }
        ],
        'nome': 'Empresa teste',
        'cnpj': '21256564000160',
        'razao_social': 'Empresa Teste LTDA',
        'tipo_servico': Empresa.ARMAZEM_DISTRIBUIDOR,
        'tipo_fornecedor': Empresa.CONVENCIONAL,
        'situacao': Empresa.SITUACAO_ATIVA,
        'cep': '04284000',
        'endereco': 'Rua América',
        'bairro': 'Vila Moinho',
        'cidade': 'São Paulo',
        'estado': 'São Paulo',
        'numero': '100',
        'complemento': ''
    }

    response = authencticated_client.post(
        '/empresas/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
