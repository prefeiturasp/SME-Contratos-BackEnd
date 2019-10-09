import pytest
from model_mommy import mommy

from ..api.serializers.empresa_serializer import EmpresaLookUpSerializer, EmpresaSerializer
from ..models.contrato import Empresa

pytestmark = pytest.mark.django_db


@pytest.fixture
def empresa():
    return mommy.make(Empresa, id=1, nome='teste', cnpj='55803656000134')


def test_empresa_serializer(empresa):
    empresa_serializer = EmpresaSerializer(empresa)

    assert empresa_serializer.data is not None
    assert 'id' not in empresa_serializer.data
    assert empresa_serializer.data['nome'] == 'teste'
    assert empresa_serializer.data['cnpj'] == '55.803.656/0001-34'
    assert empresa_serializer.data['uuid']


def test_empresa_lookup_serializer(empresa):
    empresa_serializer = EmpresaLookUpSerializer(empresa)

    assert empresa_serializer.data is not None
    assert list(empresa_serializer.data.keys()) == ['nome', 'uuid']
    assert empresa_serializer.data['nome'] == 'teste'
