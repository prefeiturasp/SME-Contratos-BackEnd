import pytest
from model_mommy import mommy

from ..models import Divisao

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make(Divisao)
    assert isinstance(model, Divisao)
    assert isinstance(model.nome, str)
    assert isinstance(model.sigla, str)


def test_srt_model():
    model = mommy.make(Divisao, nome='Divisão de Gestão de Contratos', sigla='DIGECON')
    assert model.__str__() == 'DIGECON-Divisão de Gestão de Contratos'


def test_meta_modelo():
    model = mommy.make(Divisao)
    assert model._meta.verbose_name == 'Divisão'
    assert model._meta.verbose_name_plural == 'Divisões'
