import pytest
from model_mommy import mommy

from ..api.serializers.divisao_serializer import DivisaoLookUpSerializer, DivisaoSerializer
from ..models.divisao import Divisao

pytestmark = pytest.mark.django_db


@pytest.fixture
def divisao(fake_user):
    return mommy.make(Divisao, id=1, sigla='dv1', nome='teste', diretor=fake_user, suplente_diretor=fake_user)


def test_divisao_lookup_serializer(divisao):
    divisao_serializer = DivisaoLookUpSerializer(divisao)

    assert divisao_serializer.data is not None
    assert 'id' not in divisao_serializer.data
    assert divisao_serializer.data['sigla'] == 'dv1'


def test_divisao_serializer(divisao):
    divisao_serializer = DivisaoSerializer(divisao)

    assert divisao_serializer.data is not None

    assert divisao_serializer.data['sigla'] == 'dv1'
    assert divisao_serializer['id']
    assert divisao_serializer['uuid']
    assert divisao_serializer['diretor']
    assert divisao_serializer['suplente_diretor']
