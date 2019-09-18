import pytest
from faker import Faker


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def authencticated_client(client, django_user_model):
    fake = Faker()
    username = fake.user_name()
    password = fake.text()
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    return client
