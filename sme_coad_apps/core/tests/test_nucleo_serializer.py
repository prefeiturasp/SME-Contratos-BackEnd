import pytest
from model_mommy import mommy

from ..api.serializers.nucleo_serializer import NucleoLookUpSerializer, NucleoSerializer
from ..models.divisao import Divisao
from ..models.nucleo import Nucleo

pytestmark = pytest.mark.django_db


@pytest.fixture
def divisao(fake_user):
    return mommy.make(Divisao, id=1, sigla='dv1', nome='teste', diretor=fake_user, suplente_diretor=fake_user)


@pytest.fixture
def nucleo(fake_user, divisao):
    return mommy.make(Nucleo, id=1, sigla='nc1', nome='nucleo teste', chefe=fake_user, suplente_chefe=fake_user,
                      divisao=divisao)


def test_nucleo_lookup_serializer(divisao, nucleo):
    nucleo_serializer = NucleoLookUpSerializer(nucleo)
    assert nucleo_serializer.data is not None
    assert 'id' not in nucleo_serializer.data
    assert nucleo_serializer.data['sigla'] == 'nc1'
    assert nucleo_serializer.data['divisao'] == {'sigla': divisao.sigla, 'uuid': str(divisao.uuid),
                                                 'nome': divisao.nome}
    assert nucleo_serializer.data['uuid']


def test_nucleo_serializer(divisao, nucleo):
    nucleo_serializer = NucleoSerializer(nucleo)
    assert nucleo_serializer.data is not None
    assert nucleo_serializer.data['sigla'] == 'nc1'
    assert nucleo_serializer.data['divisao'] == {'sigla': divisao.sigla, 'uuid': str(divisao.uuid),
                                                 'nome': divisao.nome}
    assert nucleo_serializer.data['uuid']
    assert nucleo_serializer.data['chefe']
    assert nucleo_serializer.data['suplente_chefe']
