import pytest
from model_mommy import mommy

from ..api.serializers.contrato_unidade_serializer import ContratoUnidadeSerializer, ContratoUnidadeLookUpSerializer

pytestmark = pytest.mark.django_db


@pytest.fixture
def contrato():
    return mommy.make('Contrato')


@pytest.fixture
def dre():
    return mommy.make('Unidade', tipo_unidade='DRE', nome='DRE Teste')


@pytest.fixture
def unidade(dre):
    return mommy.make('Unidade', tipo_unidade='CEU', dre=dre)


@pytest.fixture
def contrato_unidade(contrato, unidade):
    return mommy.make('ContratoUnidade', contrato=contrato, unidade=unidade, valor_mensal=2000.00,
                      valor_total=10000.00, lote='Lote teste')


def test_contrato_unidade_serializer(contrato, unidade, contrato_unidade):

    serializer = ContratoUnidadeSerializer(contrato_unidade)

    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['unidade']
    assert serializer.data['valor_mensal']
    assert serializer.data['valor_total']
    assert serializer.data['lote']


def test_contrato_unidade_lookup_serializer(contrato, unidade, contrato_unidade):
    serializer = ContratoUnidadeLookUpSerializer(contrato_unidade)

    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['unidade']
    assert serializer.data['valor_mensal']
    assert serializer.data['valor_total']
    assert serializer.data['lote']
    assert serializer.data['unidade']['dre']
