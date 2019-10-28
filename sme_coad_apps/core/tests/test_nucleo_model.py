import pytest
from django.contrib import admin
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..admin import NucleoAdmin
from ..models import Nucleo, Divisao

pytestmark = pytest.mark.django_db


def test_instance_model():
    user = mommy.make(User)
    model = mommy.make(Nucleo, chefe=user, suplente_chefe=user)
    assert isinstance(model, Nucleo)
    assert isinstance(model.nome, str)
    assert isinstance(model.sigla, str)
    assert isinstance(model.divisao, Divisao)
    assert model.historico
    assert isinstance(model.chefe, User)
    assert isinstance(model.suplente_chefe, User)
    assert model.servidores


def test_str_model():
    divisao = mommy.make(Divisao, sigla='DIGECON')
    model = mommy.make(Nucleo, nome='Núcleo de Unidades Administrativas', sigla='NUAD', divisao=divisao)
    assert model.__str__() == 'DIGECON/NUAD-Núcleo de Unidades Administrativas'


def test_meta_model():
    model = mommy.make(Nucleo)
    assert model._meta.verbose_name == 'Núcleo'
    assert model._meta.verbose_name_plural == 'Núcleos'


def test_admin():
    model_admin = NucleoAdmin(Divisao, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Nucleo]
    assert model_admin.list_display == ('sigla', 'nome', 'divisao')
    assert model_admin.ordering == ('divisao__sigla', 'sigla',)
    assert model_admin.search_fields == ('sigla', 'nome')
