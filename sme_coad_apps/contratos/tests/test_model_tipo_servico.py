import pytest

from model_mommy import mommy
from faker import Faker

from ..models import TipoServico

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make('TipoServico', nome='Limpeza')
    assert isinstance(model, TipoServico)
    assert isinstance(model.nome, str)


def test_srt_model():
    model = mommy.make('TipoServico', nome='Limpeza')
    assert model.__str__() == 'Limpeza'


def test_meta_modelo():
    model = mommy.make('TipoServico')
    assert model._meta.verbose_name == 'Tipo de Serviço'
    assert model._meta.verbose_name_plural == 'Tipos de Serviço'

