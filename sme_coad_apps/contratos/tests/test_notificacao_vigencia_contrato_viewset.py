from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.notificacao_vigencia_contrato_viewsets import (
    GeraNotificacoesVigenciaContratosViewSet,
    MinhasNotificacoesVigenciaViewSet
)


def test_gera_notificacoes_contratos_view_set(fake_user):
    request = APIRequestFactory().get('')
    viewset = GeraNotificacoesVigenciaContratosViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)

    response = viewset(request)

    assert response.status_code == status.HTTP_202_ACCEPTED


def test_minhas_notificacoes_view_set(fake_user):
    request = APIRequestFactory().get('')
    viewset = MinhasNotificacoesVigenciaViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=fake_user)

    response = viewset(request)

    assert response.status_code == status.HTTP_200_OK
