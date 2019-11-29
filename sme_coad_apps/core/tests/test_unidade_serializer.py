import pytest
from model_mommy import mommy

from ..api.serializers.unidade_serializer import UnidadeSerializer, UnidadeLookUpSerializer
from ..models.unidade import Unidade

pytestmark = pytest.mark.django_db


@pytest.fixture
def dre():
    return mommy.make(Unidade, tipo_unidade='DRE', nome='DRE Teste')


@pytest.fixture
def unidade(dre):
    return mommy.make(Unidade, tipo_unidade='CEU', dre=dre)


def test_unidade_lookup_serializer(unidade):
    unidade_serializer = UnidadeLookUpSerializer(unidade)

    assert unidade_serializer.data is not None
    assert 'id' not in unidade_serializer.data


def test_unidade_serializer(unidade):
    unidade_serializer = UnidadeSerializer(unidade)

    assert unidade_serializer.data is not None
    assert 'id' not in unidade_serializer.data
    assert unidade_serializer.data['dre']
