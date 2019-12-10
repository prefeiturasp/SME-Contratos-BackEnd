import pytest
from model_mommy import mommy

from ..api.serializers.fiscal_contrato_unidade_serializer import FiscalContratoUnidadeSerializer
from ..models.contrato import FiscaisUnidade

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


@pytest.fixture
def fiscal_contrato_unidade(contrato_unidade, fake_user):
    return mommy.make('FiscaisUnidade', contrato_unidade=contrato_unidade, tipo_fiscal=FiscaisUnidade.FISCAL_TITULAR,
                      fiscal=fake_user)


def test_fiscal_contrato_unidade_serializer(fiscal_contrato_unidade):
    serializer = FiscalContratoUnidadeSerializer(fiscal_contrato_unidade)

    assert serializer.data is not None
    assert serializer.data['contrato_unidade']
    assert serializer.data['tipo_fiscal']
    assert serializer.data['fiscal']
