import pytest
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..api.serializers.coad_serializer import CoadSerializer
from ..models import Coad

pytestmark = pytest.mark.django_db


def test_coad_serializer():
    coordenador = mommy.make(User)
    model = Coad.objects.create(coordenador=coordenador)

    serializer = CoadSerializer(model)

    assert serializer.data is not None
    assert serializer.data['coordenador']
