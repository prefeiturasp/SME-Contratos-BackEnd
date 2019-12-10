import json

import pytest
from faker import Faker
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.modelo_ateste_serializer import ModeloAtesteSerializer

pytestmark = pytest.mark.django_db


def test_modelo_ateste_serializer():
    modelo_ateste = mommy.make('ModeloAteste', titulo='teste')

    serializer = ModeloAtesteSerializer(modelo_ateste)

    assert serializer.data is not None
    assert serializer.data['titulo']


@pytest.fixture
def payload_modelo_ateste():
    payload = {
        'titulo': Faker().name(),
        'grupos_de_verificacao': [
            {'nome': Faker().name(),
             'itens_de_verificacao': [
                 {'item': 1, 'descricao': Faker().text()},
                 {'item': 2, 'descricao': Faker().text()},
                 {'item': 3, 'descricao': Faker().text()},
             ]
             }
        ]
    }

    return payload


def test_modelo_ateste_serializer_create(authencticated_client, payload_modelo_ateste):
    response = authencticated_client.post('/modelo-ateste/', data=json.dumps(payload_modelo_ateste),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
