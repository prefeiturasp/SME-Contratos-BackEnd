import pytest
from model_mommy import mommy

from ..api.serializers.colunas_contrato_serializer import ColunasContratoSerializer
from ..models.colunas_contrato import ColunasContrato

pytestmark = pytest.mark.django_db


def test_colunas_contrato_serializer(fake_user):
    array_campos = ['teste1', 'teste2']
    colunas_contrato = mommy.make(ColunasContrato, id='1', usuario=fake_user, colunas_array=array_campos)

    colunas_contrato_serializer = ColunasContratoSerializer(colunas_contrato)

    assert colunas_contrato_serializer.data is not None
    assert 'id' not in colunas_contrato_serializer.data
    assert colunas_contrato_serializer.data['usuario'] == fake_user.id
    assert colunas_contrato_serializer.data['colunas_array']
