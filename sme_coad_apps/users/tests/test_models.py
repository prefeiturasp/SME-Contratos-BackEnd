import pytest
from django.conf import settings
from faker import Faker
from model_mommy import mommy

from sme_coad_apps.users.models import User

pytestmark = pytest.mark.django_db

nome = Faker().name()
user_name = Faker().user_name()
model_user = settings.AUTH_USER_MODEL


def test_model_instance():
    model = mommy.make(model_user, nome=nome, username=user_name)
    assert isinstance(model, User)
    assert model.__str__() == model.nome


def test_model_verboses_names():
    model = mommy.make(model_user, nome=nome, username=user_name)
    assert model._meta.verbose_name == 'Usuário'
    assert model._meta.verbose_name_plural == 'Usuários'


def test_user_model():
    model = mommy.make(model_user, nome=nome, username=user_name)
    assert isinstance(model.nome, str)
    assert isinstance(model.__str__(), str)
    assert model.nome == nome
