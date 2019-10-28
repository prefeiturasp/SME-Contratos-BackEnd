import pytest
from django.contrib import admin
from model_mommy import mommy

from sme_coad_apps.users.models import User

from ..admin import ServidorAdmin
from ..models.servidor import Servidor

pytestmark = pytest.mark.django_db


def test_instance_model():
    servidor = mommy.make(User)
    model = mommy.make(Servidor, servidor=servidor)
    assert isinstance(model, Servidor)
    assert isinstance(model.servidor, User)
    assert model.historico


def test_srt_model():
    servidor = mommy.make(User, nome='Teste')
    model = mommy.make(Servidor, servidor=servidor)
    assert model.__str__() == "Teste"


def test_meta_modelo():
    servidor = mommy.make(User, nome='Teste')
    model = mommy.make(Servidor, servidor=servidor)
    assert model._meta.verbose_name == 'Servidor'
    assert model._meta.verbose_name_plural == 'Servidores'


def test_admin():
    model_admin = ServidorAdmin(Servidor, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Servidor]
