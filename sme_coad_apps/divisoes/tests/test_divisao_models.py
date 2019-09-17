import pytest
from model_mommy import mommy
from faker import Faker

from sme_coad_apps.divisoes.models import Divisao

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make('Divisao', nome='kelwy', sigla=Faker().user_name())
    assert isinstance(model, Divisao)
    assert isinstance(model.nome, str)


def test_srt_model():
    model = mommy.make('Divisao', nome='kelwy', sigla=Faker().user_name())
    assert model.__str__() == 'kelwy'
    assert not model.__str__() == 'Kelwy'


def test_quantidade_divisoes():
    model = mommy.make('Divisao', _quantity=10)
    assert len(model) == 10


def test_meta_modelo():
    model = mommy.make('Divisao')
    assert model._meta.verbose_name == 'Divisão'
    assert model._meta.verbose_name_plural == 'Divisões'
    assert isinstance(model._meta.verbose_name, str)
