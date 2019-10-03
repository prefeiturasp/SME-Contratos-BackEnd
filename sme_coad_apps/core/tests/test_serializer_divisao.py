import pytest
from model_mommy import mommy

from ..api.serializers.divisao_serializer import DivisaoSerializer
from ..models.divisao import Divisao

pytestmark = pytest.mark.django_db


def test_divisao_serializer():
    divisao = mommy.make(Divisao, id=1, sigla='dv1', nome='teste')

    divisao_serializer = DivisaoSerializer(divisao)

    assert divisao_serializer.data is not None
    assert divisao_serializer.data['id'] == 1
    assert divisao_serializer.data['nome'] == 'teste'
    assert divisao_serializer.data['sigla'] == 'dv1'
