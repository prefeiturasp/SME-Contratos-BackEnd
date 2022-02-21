import pytest
from faker import Faker
from model_mommy import mommy

from sme_coad_apps.users.models import User


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def contrato():
    mommy.make(User,
               username='1111111',
               nome='Galvão Bueno')
    mommy.make(User,
               username='1234567',
               nome='Calvin Feitosa')
    mommy.make('Unidade',
               codigo_eol='108101')
    mommy.make('TipoServico',
               nome='Teste tipo servico',
               uuid='7baa3356-599f-4627-9fed-832ee888de14')
    return mommy.make('Contrato',
                      uuid='d0260b07-4ed3-4741-8844-c5c3a9279f55')


@pytest.fixture
def authencticated_client(client, django_user_model):
    fake = Faker()
    username = fake.user_name()
    password = fake.text()
    u = django_user_model.objects.create_user(username=username, password=password)
    u.validado = True
    u.save()
    client.login(username=username, password=password)
    return client


@pytest.fixture
def fake_user(client, django_user_model):
    username = 'teste'
    password = 'teste'
    nome = 'teste'
    email = 'teste@teste.com'
    user = django_user_model.objects.create_user(username=username, password=password, validado=True, nome=nome,
                                                 email=email)
    client.login(username=username, password=password)
    return user


@pytest.fixture
def colunas_contrato(fake_user):
    return mommy.make('ColunasContrato',
                      uuid='d0260b07-4ed3-4741-8844-c5c3a9279f55',
                      usuario=fake_user,
                      colunas_array=[
                        {
                            "field": "termo_contrato",
                            "header": "TC"
                        },
                        {
                            "field": "processo",
                            "header": "Processo"
                        }
                      ])
