import pytest
from model_mommy import mommy
from faker import Faker

pytestmark = pytest.mark.django_db


def test_str_model():
    nome = Faker().name()
    model = mommy.make('Nucleo', nome=nome)
    assert model.__str__() == nome


def test_quantidade_model():
    model = mommy.make('Nucleo', _quantity=10)
    assert len(model) == 10


def test_meta_model():
    nome = Faker().name()
    model = mommy.make('Nucleo', nome=nome)
    assert model._meta.verbose_name == 'Núcleo'
    assert model._meta.verbose_name_plural == 'Núcleos'
