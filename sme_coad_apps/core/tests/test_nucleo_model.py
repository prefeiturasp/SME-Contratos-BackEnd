import pytest
from model_mommy import mommy

from ..models import Nucleo, Divisao

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make(Nucleo)
    assert isinstance(model, Nucleo)
    assert isinstance(model.nome, str)
    assert isinstance(model.sigla, str)
    assert isinstance(model.divisao, Divisao)


def test_str_model():
    divisao = mommy.make(Divisao, sigla='DIGECON')
    model = mommy.make(Nucleo, nome='Núcleo de Unidades Administrativas', sigla='NUAD', divisao=divisao)
    assert model.__str__() == 'DIGECON/NUAD-Núcleo de Unidades Administrativas'


def test_meta_model():
    model = mommy.make(Nucleo)
    assert model._meta.verbose_name == 'Núcleo'
    assert model._meta.verbose_name_plural == 'Núcleos'
