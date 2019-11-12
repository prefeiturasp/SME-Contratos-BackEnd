from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ..api.viewsets.services_viewsets import GeraNotificacoesVigenciaContratosViewSet


def test_gera_notificacoes_contratos_view_set(fake_user):
    request = APIRequestFactory().get("")
    viewset = GeraNotificacoesVigenciaContratosViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)

    response = viewset(request)

    assert response.status_code == status.HTTP_202_ACCEPTED
