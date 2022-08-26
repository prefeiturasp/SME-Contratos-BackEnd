import datetime
import json

import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.exceptions import ValidationError

from ..api.validations.contrato_validations import validacao_data_rescisao
from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_url_rescisao_unauthorized(client):
    response = client.get('/intercorrencias/rescisao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_rescisao_authorized(authencticated_client):
    response = authencticated_client.get('/intercorrencias/rescisao/')
    assert response.status_code == status.HTTP_200_OK


def test_url_unauthorized_lista_motivos(client):
    response = client.get('/intercorrencias/rescisao/motivos-rescisao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized_lista_motivos(authencticated_client):
    response = authencticated_client.get('/intercorrencias/rescisao/motivos-rescisao/')
    assert response.status_code == status.HTTP_200_OK


def test_post_intercorrencia_valida_payload(authencticated_client):
    contrato = mommy.make(
        Contrato,
        termo_contrato='00/00',
        criado_em=datetime.date(2019, 10, 1),
        data_assinatura=datetime.date(2019, 10, 1),
        referencia_encerramento='DATA_ASSINATURA'
    )
    payload = {
        'contrato': str(contrato.uuid),
        'tipo_intercorrencia': 'RESCISAO',
        'data_rescisao': '2014-08-22',
        'motivo_rescisao': ['DESCUMPRIMENTO_CLAUSULAS', 'LENTIDAO_NO_CUMPRIMENTO'],
    }

    response = authencticated_client.post(
        '/intercorrencias/rescisao/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    with pytest.raises(ValidationError, match='Data de rescisão anteior a data de início do contrato'):
        attrs = {'contrato': contrato, 'data_rescisao': datetime.date(2014, 8, 22)}
        validacao_data_rescisao(attrs)


def test_url_suspensao_unauthorized(client):
    response = client.get('/intercorrencias/suspensao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_suspensao_authorized(authencticated_client):
    response = authencticated_client.get('/intercorrencias/suspensao/')
    assert response.status_code == status.HTTP_200_OK


def test_url_suspensao_unauthorized_lista_motivos(client):
    response = client.get('/intercorrencias/suspensao/motivos-suspensao/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_suspensao_authorized_lista_motivos(authencticated_client):
    response = authencticated_client.get('/intercorrencias/suspensao/motivos-suspensao/')
    assert response.status_code == status.HTTP_200_OK


def test_post_intercorrencia_suspensao_valida_payload(authencticated_client):
    contrato = mommy.make(
        Contrato,
        termo_contrato='00/00',
        criado_em=datetime.date(2019, 10, 1),
    )
    payload = {
        'contrato': str(contrato.uuid),
        'tipo_intercorrencia': 'SUSPENSAO',
        'data_inicial': '2022-08-26',
        'data_final': '2022-09-20',
        'acrescentar_dias': True,
        'motivo_suspensao': 'UNILATERALMENTE_ADMINISTRACAO_PUBLICA',
        'opcao_suspensao': 'Conveniência da Administração Pública',
        'descricao_suspensao': 'Teste de descrição de post'
    }

    response = authencticated_client.post(
        '/intercorrencias/suspensao/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED
