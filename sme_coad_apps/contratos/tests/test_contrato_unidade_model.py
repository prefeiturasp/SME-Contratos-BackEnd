import pytest
from model_mommy import mommy

from sme_coad_apps.core.models import Unidade
from ..models.contrato import ContratoUnidade, Contrato

pytestmark = pytest.mark.django_db


def test_instance_model():
    contrato = mommy.make('Contrato')
    unidade = mommy.make('Unidade')
    contrato_unidade = mommy.make('ContratoUnidade', contrato=contrato, unidade=unidade)

    assert isinstance(contrato_unidade, ContratoUnidade)
    assert isinstance(contrato_unidade.contrato, Contrato)
    assert isinstance(contrato_unidade.unidade, Unidade)
    assert isinstance(contrato_unidade.valor_mensal, float)
    assert isinstance(contrato_unidade.valor_total, float)
    assert isinstance(contrato_unidade.lote, str)
    assert isinstance(contrato_unidade.dre_lote, str)
