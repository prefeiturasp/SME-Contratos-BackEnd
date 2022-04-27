import json

import pytest
from rest_framework import status

from sme_coad_apps.contratos.models import Empresa

pytestmark = pytest.mark.django_db


@pytest.fixture
def payload_empresa(authencticated_client):
    payload = {
        'contatos': [
            {
                'nome': 'Empresa teste',
                'email': 'user@example.com',
                'telefone': '11999999999',
                'cargo': 'Gerente'
            }
        ],
        'nome': 'EmpresaTeste',
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

    return payload


@pytest.fixture
def test_post_empresa(authencticated_client, payload_empresa):

    response = authencticated_client.post(
        '/empresas/',
        data=json.dumps(payload_empresa),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    return response


def test_get_ata_filters(authencticated_client, test_post_empresa):
    result = json.loads(test_post_empresa.content)
    rota = f"""/empresas/?nome={result['nome']}
                &status=ATIVA
                &cnpj_empresa={result['cnpj']}
                &tipo_servico=FORNECEDOR
                &tipo_fornecedor=CONVENCIONAL"""

    url = rota.replace('\n', '').replace(' ', '')
    response = authencticated_client.get(url, content_type='application/json')
    resposta = json.loads(response.content)
    esperado = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'uuid': f"{result['uuid']}",
                'nome': f"{result['nome']}",
                'id': resposta['results'][0]['id'],
                'cnpj': '21.256.564/0001-60',
                'situacao': 'Ativa',
                'tipo_servico': 'Fornecedor'
            }
        ]
    }
    assert resposta == esperado
