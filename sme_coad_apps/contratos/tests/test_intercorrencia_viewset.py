import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.intercorrencia_serializer import RescisaoSerializer, SuspensaoSerializer
from ..models import Contrato, Rescisao, Suspensao

pytestmark = pytest.mark.django_db


def test_intercorrencia_serializer_rescisao(rescisao):
    serializer = RescisaoSerializer(rescisao)
    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['tipo_intercorrencia'] == 'RESCISAO'
    assert serializer.data['data_rescisao']
    assert serializer.data['motivo_rescisao']


def test_intercorrencia_serializer_suspensao(suspensao):
    serializer = SuspensaoSerializer(suspensao)
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
def payload_intercorrencia_rescisao():
    contrato = mommy.make(Contrato, id=1, termo_contrato='1234/2022')
    payload = {
        'tipo_intercorrencia': Rescisao.TIPO_INTERCORRENCIA_RESCISAO,
        'data_rescisao': '2022-08-26',
        'motivo_rescisao': [Rescisao.MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS,
                            Rescisao.MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO],
        'contrato': str(contrato.uuid)
    }
    return payload


@pytest.fixture
def test_intercorrencia_serializer_create_rescisao(authencticated_client, payload_intercorrencia_rescisao):
    response = authencticated_client.post('/intercorrencias/rescisao/',
                                          data=json.dumps(payload_intercorrencia_rescisao),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response


@pytest.fixture
def payload_intercorrencia_suspensao():
    contrato = mommy.make(Contrato, id=1, termo_contrato='1234/2022')
    payload = {
        'tipo_intercorrencia': Suspensao.TIPO_INTERCORRENCIA_SUSPENSAO,
        'data_inicial': '2022-08-26',
        'data_final': '2022-09-20',
        'acrescentar_dias': True,
        'motivo_suspensao': Suspensao.MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA,
        'opcao_suspensao': 'Conveniência da Administração Pública',
        'descricao_suspensao': 'Teste de descrição de post',
        'contrato': str(contrato.uuid)
    }
    return payload


@pytest.fixture
def test_intercorrencia_serializer_create_suspensao(authencticated_client, payload_intercorrencia_suspensao):
    response = authencticated_client.post('/intercorrencias/suspensao/',
                                          data=json.dumps(payload_intercorrencia_suspensao),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response
