import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.intercorrencia_serializer import ImpedimentoSerializer, RescisaoSerializer, SuspensaoSerializer
from ..models import Contrato, Impedimento, Rescisao, Suspensao

pytestmark = pytest.mark.django_db


def test_intercorrencia_serializer_impedimento(impedimento):
    serializer = ImpedimentoSerializer(impedimento)
    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['tipo_intercorrencia'] == 'Impedimento'
    assert serializer.data['data_inicial']
    assert serializer.data['data_final']
    assert serializer.data['descricao_impedimento']


@pytest.fixture
def payload_intercorrencia_impedimento():
    contrato = mommy.make(Contrato, id=1, termo_contrato='1234/2022')
    payload = {
        'tipo_intercorrencia': Impedimento.TIPO_INTERCORRENCIA_IMPEDIMENTO,
        'data_inicial': '2022-08-26',
        'data_final': '2022-09-20',
        'descricao_impedimento': 'Teste de descrição de impedimento',
        'contrato': str(contrato.uuid)
    }
    return payload


@pytest.fixture
def test_intercorrencia_serializer_create_impedimento(authencticated_client, payload_intercorrencia_impedimento):
    response = authencticated_client.post('/intercorrencias/impedimento/',
                                          data=json.dumps(payload_intercorrencia_impedimento),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response


def test_intercorrencia_serializer_rescisao(rescisao):
    serializer = RescisaoSerializer(rescisao)
    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['tipo_intercorrencia'] == 'Rescisão'
    assert serializer.data['data_rescisao']
    assert serializer.data['motivo_rescisao']


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


def test_intercorrencia_serializer_suspensao(suspensao):
    serializer = SuspensaoSerializer(suspensao)
    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['tipo_intercorrencia'] == 'Suspensão'
    assert serializer.data['data_inicial']
    assert serializer.data['data_final']
    assert serializer.data['acrescentar_dias']
    assert serializer.data['motivo_suspensao']
    assert serializer.data['opcao_suspensao']
    assert serializer.data['descricao_suspensao']


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
        'descricao_suspensao': 'Teste de descrição de suspensão',
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
