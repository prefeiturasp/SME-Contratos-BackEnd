import pytest
from model_mommy import mommy

from ..api.serializers.contrato_unidade_serializer import ContratoUnidadeSerializer

pytestmark = pytest.mark.django_db


def test_contrato_unidade_serializer():
    contrato = mommy.make('Contrato')
    unidade = mommy.make('Unidade')
    contrato_unidade = mommy.make('ContratoUnidade', contrato=contrato, unidade=unidade, valor_mensal=2000.00,
                                  valor_total=10000.00, lote='Lote teste',
                                  dre_lote='DTC')
    serializer = ContratoUnidadeSerializer(contrato_unidade)

    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['unidade']
    assert serializer.data['valor_mensal']
    assert serializer.data['valor_total']
    assert serializer.data['lote']
    assert serializer.data['dre_lote']
