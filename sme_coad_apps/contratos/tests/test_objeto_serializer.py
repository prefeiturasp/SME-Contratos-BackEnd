import pytest
from model_mommy import mommy

from ..api.serializers.objeto_serializer import ObjetoLookupSerializer, ObjetoSerializer
from ..models.contrato import Objeto

pytestmark = pytest.mark.django_db


def test_objeto_serializer():
    objeto = mommy.make(Objeto, id=1, nome='teste')

    objeto_serializer = ObjetoSerializer(objeto)

    assert objeto_serializer.data is not None
    assert 'id' not in objeto_serializer.data
    assert objeto_serializer.data['nome'] == 'teste'
    assert objeto_serializer.data['uuid']


def test_objeto_lookup_serializer():
    objeto = mommy.make(Objeto, id=1, nome='teste')

    objeto_serializer = ObjetoLookupSerializer(objeto)

    assert objeto_serializer.data is not None
    # TODO Remover id do serializer
    # assert 'id' not in objeto_serializer.data
    assert objeto_serializer.data['id']
    assert objeto_serializer.data['nome'] == 'teste'
    assert objeto_serializer.data['uuid']
