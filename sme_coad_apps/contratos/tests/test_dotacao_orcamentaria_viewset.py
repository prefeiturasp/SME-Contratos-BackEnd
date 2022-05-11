import json

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.dotacao_valor_viewset import DotacaoOrcamentariaViewSet

pytestmark = pytest.mark.django_db


def test_dotacao_orcamentaria_viewset(fake_user, dotacao_orcamentaria):
    request = APIRequestFactory().get('')
    dotacao_orcamentaria_detalhe = DotacaoOrcamentariaViewSet.as_view({'get': 'retrieve'})
    dotacao_orcamentaria_lista = DotacaoOrcamentariaViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)

    response = dotacao_orcamentaria_detalhe(request, uuid=dotacao_orcamentaria.uuid)
    response2 = dotacao_orcamentaria_lista(request)

    assert response.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK


@pytest.fixture
def payload_dotacao_orcamentaria():
    payload = {
        'orgao': '99',
        'unidade': '88',
        'funcao': '77',
        'subfuncao': '666',
        'programa': '5555',
        'projeto_atividade': '4.444',
        'conta_despesa': '33333333',
        'fonte': '22'
    }
    return payload


def test_dotacao_orcamentaria_create(authencticated_client, payload_dotacao_orcamentaria):
    response = authencticated_client.post('/dotacoes-orcamentarias/', data=json.dumps(payload_dotacao_orcamentaria),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    return response
