import pytest
from model_mommy import mommy

from ..api.serializers.empresa_serializer import EmpresaLookUpSerializer
from ..models.contrato import Empresa

pytestmark = pytest.mark.django_db


def test_empresa_serializer():
    empresa = mommy.make(Empresa, id=1, nome='teste', cnpj='55803656000134')

    empresa_serializer = EmpresaLookUpSerializer(empresa)

    assert empresa_serializer.data is not None
    assert empresa_serializer.data['id'] == 1
    assert empresa_serializer.data['nome'] == 'teste'
    assert empresa_serializer.data['cnpj'] == '55.803.656/0001-34'
