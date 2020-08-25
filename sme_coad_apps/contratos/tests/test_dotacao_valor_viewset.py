import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.dotacao_valor_viewset import DotacaoValorViewSet

pytestmark = pytest.mark.django_db


def test_dotacao_valor_viewset(fake_user):
    request = APIRequestFactory().get("")
    dotacao_valor_detalhe = DotacaoValorViewSet.as_view({'get': 'retrieve'})
    dotacao_valor_lista = DotacaoValorViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)
    model = mommy.make('DotacaoValor')
    contrato = mommy.make('Contrato')

    response = dotacao_valor_detalhe(request, uuid=model.uuid)
    response2 = dotacao_valor_lista(request, contrato__uuid=contrato.uuid)

    assert response.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
