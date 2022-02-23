import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.colunas_contrato_viewset import ColunasContratoViewSet

pytestmark = pytest.mark.django_db

def test_colunas_contrato_view_set(fake_user, colunas_contrato):
    request = APIRequestFactory().get("")
    colunas_contrato_detalhe = ColunasContratoViewSet.as_view({'get': 'retrieve'})
    force_authenticate(request, user=fake_user)

    response = colunas_contrato_detalhe(request, uuid=colunas_contrato.uuid)

    assert response.status_code == status.HTTP_200_OK
