import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ..api.viewsets.colunas_contrato_viewset import ColunasContratoViewSet
from ..models.colunas_contrato import ColunasContrato

# pytestmark = pytest.mark.django_db

# TODO Teste falhando por incompatibilidade do pytest com JSONFild
# def test_colunas_contrato_view_set(fake_user):
#     request = APIRequestFactory().get("")
#     tipo_servico_detalhe = ColunasContratoViewSet.as_view({'get': 'retrieve'})
#     force_authenticate(request, user=fake_user)
#     colunas_contrato = mommy.make(ColunasContrato)
#
#     response = tipo_servico_detalhe(request, uuid=colunas_contrato.uuid)
#
#     assert response.status_code == status.HTTP_200_OK
