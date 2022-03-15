import pytest
from model_mommy import mommy

from sme_coad_apps.core.models import Unidade

from ..models.contrato import Contrato, ContratoUnidade, FiscaisUnidade

pytestmark = pytest.mark.django_db


@pytest.fixture
def contrato():
    return mommy.make('Contrato', termo_contrato='10/10')


@pytest.fixture
def unidade():
    return mommy.make('Unidade', nome='Unidade Teste')


@pytest.fixture
def contrato_unidade(contrato, unidade):
    return mommy.make('ContratoUnidade', contrato=contrato, unidade=unidade)


@pytest.fixture
def fiscais_unidade(contrato_unidade, fake_user):
    return mommy.make('FiscaisUnidade', contrato_unidade=contrato_unidade, fiscal=fake_user, tipo_fiscal='TITULAR')


def test_instance_contrato_unidade(contrato_unidade):
    assert isinstance(contrato_unidade, ContratoUnidade)
    assert isinstance(contrato_unidade.contrato, Contrato)
    assert isinstance(contrato_unidade.unidade, Unidade)
    assert isinstance(contrato_unidade.valor_mensal, float)
    assert isinstance(contrato_unidade.valor_total, float)
    assert isinstance(contrato_unidade.lote, str)


def test_instance_fiscais_unidade(fiscais_unidade):
    assert isinstance(fiscais_unidade, FiscaisUnidade)
    assert FiscaisUnidade.objects.exists()


def test_srt_fiscais_unidade(fiscais_unidade, fake_user):
    assert fiscais_unidade.__str__() == f'Fiscal (TITULAR): {fake_user.nome} do TC:10/10 na unidade: Unidade Teste'


def test_meta_modelo_fiscais_unidade(fiscais_unidade):
    assert fiscais_unidade._meta.verbose_name == 'Fiscal da Unidade de Contrato'
    assert fiscais_unidade._meta.verbose_name_plural == 'Fiscais das Unidades de Contratos'
