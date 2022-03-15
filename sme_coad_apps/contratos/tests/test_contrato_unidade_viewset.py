import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from sme_coad_apps.contratos.api.viewsets.contrato_unidade_viewset import ContratoUnidadeViewSet

pytestmark = pytest.mark.django_db


def test_contrato_unidade_viewset(fake_user):
    request = APIRequestFactory().get('')
    contrato_unidade_detalhe = ContratoUnidadeViewSet.as_view({'get': 'retrieve'})
    contrato_unidade_lista = ContratoUnidadeViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)
    model = mommy.make('ContratoUnidade')
    contrato = mommy.make('Contrato')

    response = contrato_unidade_detalhe(request, uuid=model.uuid)
    response2 = contrato_unidade_lista(request, contrato__uuid=contrato.uuid)

    assert response.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
