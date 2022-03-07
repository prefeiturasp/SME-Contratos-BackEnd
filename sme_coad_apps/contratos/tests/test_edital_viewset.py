import json

import pytest
from faker import Faker
from model_mommy import mommy
from rest_framework import status

from ..api.serializers.edital_serializer import EditalSerializer

pytestmark = pytest.mark.django_db


def test_edital_serializer():
    edital = mommy.make('Edital', numero='10/SME/2020')

    serializer = EditalSerializer(edital)

    assert serializer.data is not None
    assert serializer.data['numero']


@pytest.fixture
def payload_edital():
    payload = {
        'numero': Faker().name(),
        'grupos_de_obrigacao': [
            {'nome': Faker().name(),
             'itens_de_obrigacao': [
                 {'item': "1", 'descricao': Faker().text()},
                 {'item': "2", 'descricao': Faker().text()},
                 {'item': "3", 'descricao': Faker().text()},
             ]
             }
        ]
    }

    return payload


def test_edital_serializer_create(authencticated_client, payload_edital):
    response = authencticated_client.post('/editais/', data=json.dumps(payload_edital),
                                          content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
