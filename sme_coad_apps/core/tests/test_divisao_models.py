import pytest
from django.contrib import admin
from model_mommy import mommy

from sme_coad_apps.users.models import User

from ..admin import DivisaoAdmin
from ..models import Divisao

pytestmark = pytest.mark.django_db


def test_instance_model():
    user = mommy.make(User)
    model = mommy.make(Divisao, diretor=user, suplente_diretor=user)
    assert isinstance(model, Divisao)
    assert isinstance(model.nome, str)
    assert isinstance(model.sigla, str)
    assert model.historico
    assert isinstance(model.diretor, User)
    assert isinstance(model.suplente_diretor, User)


def test_srt_model():
    model = mommy.make(Divisao, nome='Divisão de Gestão de Contratos', sigla='DIGECON')
    assert model.__str__() == 'DIGECON-Divisão de Gestão de Contratos'


def test_meta_modelo():
    model = mommy.make(Divisao)
    assert model._meta.verbose_name == 'Divisão'
    assert model._meta.verbose_name_plural == 'Divisões'


def test_admin():
    model_admin = DivisaoAdmin(Divisao, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Divisao]
    assert model_admin.list_display == ('sigla', 'nome')
    assert model_admin.ordering == ('sigla',)
    assert model_admin.search_fields == ('sigla', 'nome')
