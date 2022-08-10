import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.aditamento_serializer import AditamentoSerializer
from ..models import Aditamento, Contrato

pytestmark = pytest.mark.django_db


def test_aditamento_serializer(aditamento):
    serializer = AditamentoSerializer(aditamento)

    assert serializer.data is not None
    assert serializer.data['termo_aditivo'] == aditamento.termo_aditivo
    assert serializer.data['objeto_aditamento']
    assert serializer.data['contrato']
    assert serializer.data['data_inicial']
    assert serializer.data['data_final']
    assert serializer.data['valor_mensal_atualizado']
    assert serializer.data['valor_total_atualizado']
    assert serializer.data['valor_aditamento']
    assert serializer.data['razoes_aditamento']


@pytest.fixture
def payload_aditamento():
    contrato = mommy.make(Contrato, id=1, termo_contrato='1234/2022')
    payload = {
        'termo_aditivo': '12345/2022',
        'objeto_aditamento': [Aditamento.OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL],
        'valor_mensal_atualizado': 1000.00,
        'valor_total_atualizado': 20000.00,
        'valor_aditamento': 10000.00,
        'data_inicial': '2023-04-06',
        'data_final': '2023-05-01',
        'contrato': str(contrato.uuid),
        'razoes_aditamento': 'Teste de aditamento'
    }
    return payload


@pytest.fixture
def test_aditamento_serializer_create(authencticated_client, payload_aditamento):
    response = authencticated_client.post('/aditamentos/', data=json.dumps(payload_aditamento),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response
