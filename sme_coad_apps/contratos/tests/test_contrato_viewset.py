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


def test_contrato_view_set_filters(fake_user):
    contrato_viewset = ContratoViewSet()

    assert contrato_viewset.ordering_fields == ('data_ordem_inicio',)
    assert contrato_viewset.filter_fields == (
        'situacao', 'tipo_servico', 'gestor', 'empresa_contratada', 'estado_contrato', 'termo_contrato')
    assert contrato_viewset.search_fields == ('processo',)
