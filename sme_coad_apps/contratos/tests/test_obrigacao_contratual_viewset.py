import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.obricacao_contratual_viewset import ObrigacaoContratualViewSet

pytestmark = pytest.mark.django_db


def test_obrigacao_contratual_viewset(fake_user):
    request = APIRequestFactory().get('')
    obrigacao_contratual_detalhe = ObrigacaoContratualViewSet.as_view({'get': 'retrieve'})
    obrigacao_contratual_lista = ObrigacaoContratualViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)
    model = mommy.make('ObrigacaoContratual')
    contrato = mommy.make('Contrato')

    response = obrigacao_contratual_detalhe(request, uuid=model.uuid)
    response2 = obrigacao_contratual_lista(request, contrato__uuid=contrato.uuid)

    assert response.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
