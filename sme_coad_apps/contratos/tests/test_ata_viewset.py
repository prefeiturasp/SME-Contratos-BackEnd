import json

import pytest
from faker import Faker
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.ata_serializer import AtaLookUpSerializer, AtaSerializer
from ..models import Ata, Edital, Produto

pytestmark = pytest.mark.django_db


def test_ata_serializer(ata):
    serializer = AtaSerializer(ata)

    assert serializer.data is not None
    assert serializer.data['numero'] == ata.numero
    assert serializer.data['status']
    assert serializer.data['vigencia']
    assert serializer.data['unidade_vigencia']
    assert serializer.data['data_assinatura']
    assert serializer.data['data_encerramento']
    assert serializer.data['edital']
    assert serializer.data['historico']


def test_ata_lookup_serializer(ata):
    serializer = AtaLookUpSerializer(ata)

    assert serializer.data is not None
    assert serializer.data['numero'] == ata.numero
    assert serializer.data['uuid']
    assert serializer.data['nome_empresa']
    assert serializer.data['status']
    assert serializer.data['data_encerramento']


@pytest.fixture
def payload_ata():
    edital = mommy.make(Edital, id=1, numero='1234/2022')
    produto = mommy.make(Produto, id=1, nome='ARROZ')
    payload = {
        'numero': Faker().name(),
        'status': Ata.ATIVA,
        'unidade_vigencia': Ata.UNIDADE_VIGENCIA_DIAS,
        'vigencia': 25,
        'data_assinatura': '2022-04-06',
        'data_encerramento': '2022-05-01',
        'edital': str(edital.uuid),
        'produtos': [
            {
                'produto': str(produto.uuid),
                'quantidade_total': '00.00',
                'valor_unitario': '10.00',
                'valor_total': '1000.00',
                'anexo': 'data:text/txt;base64,W1tzb3VyY2VdXQp1cmwgPSAiaHR0cHM6Ly9weXBpLnB5dGhvbi5vcmcvc2ltcGxlIgp/'
                         '2ZXJpZnlfc3NsID0gdHJ1ZQpuYW1lID0gInB5cGkiCgpbcGFja2FnZXNdCgpbZGV2LXBhY2thZ2VzXQoKW3JlcXV/'
                         'pcmVzXQpweXRob25fdmVyc2lvbiA9ICIzLjYiCg=='
            }
        ]
    }
    return payload


@pytest.fixture
def test_ata_serializer_create(authencticated_client, payload_ata):
    response = authencticated_client.post('/atas/', data=json.dumps(payload_ata),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response


def test_get_ata_filters(authencticated_client, test_ata_serializer_create):
    result = json.loads(test_ata_serializer_create.content)
    rota = f"""/atas/?data_final={result['data_encerramento']}
                &status=ATIVA
                &data_final={result['data_encerramento']}
                &numero={result['numero']}"""

    url = rota.replace('\n', '')
    response = authencticated_client.get(url, content_type='application/json')
    resposta = json.loads(response.content)

    assert resposta
    assert resposta['count'] == 1
    assert resposta['results']
