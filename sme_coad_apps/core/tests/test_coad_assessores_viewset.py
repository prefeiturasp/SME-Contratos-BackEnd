import pytest
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from ..api.viewsets.coad_assessor_viewset import CoadAssessorViewSet
from ..models import CoadAssessor

pytestmark = pytest.mark.django_db


def test_view_set(fake_user):
    request = APIRequestFactory().get("")
    detalhe = CoadAssessorViewSet.as_view({'get': 'retrieve'})
    force_authenticate(request, user=fake_user)
    model = mommy.make(CoadAssessor)

    response = detalhe(request, pk=model.pk)

    assert response.status_code == status.HTTP_200_OK
