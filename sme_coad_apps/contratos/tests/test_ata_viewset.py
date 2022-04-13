import json

import pytest
from faker import Faker
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.ata_serializer import AtaSerializer
from ..models import Ata, Edital

pytestmark = pytest.mark.django_db


def test_edital_serializer(ata):
    serializer = AtaSerializer(ata)

    assert serializer.data is not None
    assert serializer.data['numero'] == ata.numero
    assert serializer.data['status']
    assert serializer.data['vigencia']
    assert serializer.data['unidade_vigencia']
    assert serializer.data['data_assinatura']
    assert serializer.data['data_encerramento']
    assert serializer.data['edital']


@pytest.fixture
def payload_ata():
    edital = mommy.make(Edital, id=1, numero='1234/2022')
    payload = {
        'numero': Faker().name(),
        'status': Ata.ATIVA,
        'unidade_vigencia': Ata.UNIDADE_VIGENCIA_DIAS,
        'vigencia': 25,
        'data_assinatura': '2022-04-06',
        'data_encerramento': '2022-05-01',
        'edital': str(edital.uuid),
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
    data = result['data_encerramento'].split('-')
    esperado = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'uuid': f"{result['uuid']}",
                'numero': f"{result['numero']}",
                'nome_empresa': None,
                'status': 'Ativa',
                'data_encerramento': f'{data[2]}/{data[1]}/{data[0]}',
                'objeto': None
            }
        ]
    }
    assert resposta == esperado
