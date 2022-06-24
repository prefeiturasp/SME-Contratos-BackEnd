import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.objeto_viewsets import ObjetoViewSet
from ..models.objeto import Objeto

pytestmark = pytest.mark.django_db


def test_objeto_view_set(fake_user):
    request = APIRequestFactory().get('')
    objeto_detalhe = ObjetoViewSet.as_view({'get': 'retrieve'})
    force_authenticate(request, user=fake_user)
    objeto = mommy.make(Objeto)

    response = objeto_detalhe(request, uuid=objeto.uuid)

    assert response.status_code == status.HTTP_200_OK
