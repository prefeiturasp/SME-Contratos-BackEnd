import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ..api.viewsets.tipo_servico_viewsets import TipoServicoViewSet
from ..models.tipo_servico import TipoServico

pytestmark = pytest.mark.django_db


def test_tipo_servico_view_set(fake_user):
    request = APIRequestFactory().get("")
    tipo_servico_detalhe = TipoServicoViewSet.as_view({'get': 'retrieve'})
    force_authenticate(request, user=fake_user)
    tipo_servico = mommy.make(TipoServico)

    response = tipo_servico_detalhe(request, uuid=tipo_servico.uuid)

    assert response.status_code == status.HTTP_200_OK
