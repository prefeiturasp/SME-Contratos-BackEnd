import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.intercorrencia_serializer import IntercorrenciaSerializer
from ..models import Contrato, Intercorrencia

pytestmark = pytest.mark.django_db


def test_intercorrencia_serializer(intercorrencia):
    serializer = IntercorrenciaSerializer(intercorrencia)

    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['tipo_intercorrencia'] == 'SUSPENSAO'
    assert serializer.data['data_inicial']
    assert serializer.data['data_final']
    assert serializer.data['acrescentar_dias']
    assert serializer.data['motivo_suspensao']
    assert serializer.data['opcao_suspensao']
    assert serializer.data['descricao_suspensao']


@pytest.fixture
def payload_intercorrencia():
    contrato = mommy.make(Contrato, id=1, termo_contrato='1234/2022')
    payload = {
        'tipo_intercorrencia': Intercorrencia.TIPO_INTERCORRENCIA_SUSPENSAO,
        'data_inicial': '2022-08-26',
        'data_final': '2022-09-20',
        'acrescentar_dias': True,
        'motivo_suspensao': Intercorrencia.MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA,
        'opcao_suspensao': 'Conveniência da Administração Pública',
        'descricao_suspensao': 'Teste de descrição de post',
        'contrato': str(contrato.uuid)
    }
    return payload


@pytest.fixture
def test_intercorrencia_serializer_create(authencticated_client, payload_intercorrencia):
    response = authencticated_client.post('/intercorrencias/', data=json.dumps(payload_intercorrencia),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response
