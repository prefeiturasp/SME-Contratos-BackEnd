import pytest
from django.contrib import admin
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..admin import ServidorAdmin
from ..models.servidor import Servidor
from ...core.models import Divisao, Nucleo

pytestmark = pytest.mark.django_db


@pytest.fixture
def divisao(fake_user):
    return mommy.make(Divisao, id=1, sigla='dv1', nome='teste', diretor=fake_user, suplente_diretor=fake_user)


@pytest.fixture
def nucleo(fake_user, divisao):
    return mommy.make(Nucleo, id=1, sigla='nc1', nome='nucleo teste', chefe=fake_user, suplente_chefe=fake_user,
                      divisao=divisao)


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


def test_append_servidor(nucleo, fake_user):
    assert nucleo.servidores.all().count() == 0
    servidores = [{'username': fake_user.username}, ]
    Servidor.append_servidores(nucleo=nucleo, servidores=servidores)
    assert nucleo.servidores.all().count() == 1


def test_limpa_servidor(nucleo, fake_user):
    mommy.make(Servidor, nucleo=nucleo, servidor=fake_user)
    assert nucleo.servidores.all().count() == 1
    Servidor.limpa_servidores(nucleo=nucleo)
    assert nucleo.servidores.all().count() == 0
