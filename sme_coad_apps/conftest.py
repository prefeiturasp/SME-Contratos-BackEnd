import pytest
from model_mommy import mommy

from .users.models import User


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def gestor():
    return mommy.make(User, username='gestor')


@pytest.fixture
def suplente():
    return mommy.make(User, username='suplente')


@pytest.fixture
def tipo_servico():
    return mommy.make('TipoServico')


@pytest.fixture
def nucleo():
    return mommy.make('Nucleo')


@pytest.fixture
def empresa():
    return mommy.make('Empresa')


@pytest.fixture
def client_autenticado(client, django_user_model):
    username = '123456'
    password = 'teste'
    validado = True
    django_user_model.objects.create_user(password=password, username=username, validado=validado)
    client.login(username=username, password=password)
    return client
