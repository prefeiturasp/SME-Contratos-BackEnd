import pytest
from model_mommy import mommy

from sme_coad_apps.users.models import User

from ..api.serializers.servidor_serializer import ServidorSerializer
from ..models import Servidor

pytestmark = pytest.mark.django_db


def test_servidor_serializer():
    servidor = mommy.make(User)
    model = mommy.make(Servidor, servidor=servidor)

    serializer = ServidorSerializer(model)

    assert serializer.data is not None
    assert serializer.data['servidor']
    assert serializer.data['nucleo']
    assert serializer.data['id']
