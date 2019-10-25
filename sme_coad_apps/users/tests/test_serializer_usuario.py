import pytest
from model_mommy import mommy

from ..api.serializers.usuario_serializer import UsuarioLookUpSerializer
from ..models import User

pytestmark = pytest.mark.django_db


def test_usuario_lookup_serializer():
    usuario = mommy.make(User, id=1, nome='teste', username='teste')

    usuario_serializer = UsuarioLookUpSerializer(usuario)

    assert usuario_serializer.data is not None
    # TODO remover id do serializer lookup
    # assert 'id' not in usuario_serializer.data
    assert usuario_serializer.data['id']
    assert usuario_serializer.data['nome'] == 'teste'
    assert usuario_serializer.data['uuid']
    assert usuario_serializer.data['username'] == 'teste'
