import pytest
from model_mommy import mommy

from ..api.serializers.divisao_serializer import DivisaoLookUpSerializer
from ..models.divisao import Divisao

pytestmark = pytest.mark.django_db


def test_divisao_lookup_serializer():
    divisao = mommy.make(Divisao, id=1, sigla='dv1', nome='teste')

    divisao_serializer = DivisaoLookUpSerializer(divisao)

    assert divisao_serializer.data is not None
    assert 'id' not in divisao_serializer.data
    assert divisao_serializer.data['sigla'] == 'dv1'
    assert divisao_serializer['uuid']
