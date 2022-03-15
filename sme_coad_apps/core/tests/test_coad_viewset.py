import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from ..api.viewsets.coad_viewset import CoadViewSet
from ..models.coad import Coad

pytestmark = pytest.mark.django_db


def test_view_set(fake_user):
    request = APIRequestFactory().get('')
    detalhe = CoadViewSet.as_view({'get': 'retrieve'})
    force_authenticate(request, user=fake_user)
    model = mommy.make(Coad)

    response = detalhe(request, pk=model.pk)

    assert response.status_code == status.HTTP_200_OK
