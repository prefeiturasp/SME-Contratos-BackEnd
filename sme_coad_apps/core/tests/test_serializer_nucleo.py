import pytest
from model_mommy import mommy

from ..api.serializers.nucleo_serializer import NucleoLookUpSerializer
from ..models.divisao import Divisao
from ..models.nucleo import Nucleo

pytestmark = pytest.mark.django_db


def test_nucleo_lookup_serializer():
    divisao = mommy.make(Divisao, id=1, sigla='dv1', nome='teste')
    nucleo = mommy.make(Nucleo, id=1, sigla='nc1', nome='teste', divisao=divisao)

    nucleo_serializer = NucleoLookUpSerializer(nucleo)

    assert nucleo_serializer.data is not None
    assert nucleo_serializer.data['id'] == 1
    assert nucleo_serializer.data['sigla'] == 'nc1'
    assert nucleo_serializer.data['divisao'] == {'id': 1, 'sigla': 'dv1'}
