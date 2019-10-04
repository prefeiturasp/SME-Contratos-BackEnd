import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ..api.viewsets.contrato_viewset import ContratoViewSet
from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_contrato_view_set(fake_user):
    request = APIRequestFactory().get("")
    contrato_detalhe = ContratoViewSet.as_view({'get': 'retrieve'})
    force_authenticate(request, user=fake_user)
    contrato = mommy.make(Contrato)

    response = contrato_detalhe(request, uuid=contrato.uuid)

    assert response.status_code == status.HTTP_200_OK