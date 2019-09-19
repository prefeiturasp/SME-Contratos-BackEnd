import pytest
from faker import Faker


@pytest.fixture
def authorizade_client(client, django_user_model):
    username = Faker().user_name()
    password = Faker().text()
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    return client
