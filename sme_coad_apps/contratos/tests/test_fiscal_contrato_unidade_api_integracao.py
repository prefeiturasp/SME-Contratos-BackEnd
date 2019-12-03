import json

import pytest
from model_mommy import mommy
from rest_framework import status

from ..models.contrato import FiscaisUnidade, ContratoUnidade

pytestmark = pytest.mark.django_db


@pytest.fixture
def contrato():
    return mommy.make('Contrato')


@pytest.fixture
def dre():
    return mommy.make('Unidade', tipo_unidade='DRE', nome='DRE Teste')


@pytest.fixture
def unidade(dre):
    return mommy.make('Unidade', tipo_unidade='CEU', dre=dre)


@pytest.fixture
def contrato_unidade(contrato, unidade):
    return mommy.make('ContratoUnidade', contrato=contrato, unidade=unidade, valor_mensal=2000.00,
                      valor_total=10000.00, lote='Lote teste')


@pytest.fixture
def fiscal_contrato_unidade(contrato_unidade, fake_user):
    return mommy.make('FiscaisUnidade', contrato_unidade=contrato_unidade, tipo_fiscal=FiscaisUnidade.FISCAL_TITULAR,
                      fiscal=fake_user)


def test_fiscal_contrato_unidade_api_retrieve(client, fiscal_contrato_unidade):
    response = client.get(f'/unidades-contratos/{fiscal_contrato_unidade.contrato_unidade.uuid}/')
    assert response.status_code == status.HTTP_200_OK
    assert str(fiscal_contrato_unidade.contrato_unidade.uuid) in response.content.decode("utf-8")


def test_fiscal_contrato_unidade_api_create(client, contrato, unidade, fake_user):
    payload = {
        "contrato": f'{contrato.uuid}',
        "unidade": f'{unidade.uuid}',
        "fiscais": [
            {
                "fiscal": f'{fake_user.uuid}',
                "tipo_fiscal": "TITULAR"
            },
            {
                "fiscal": f'{fake_user.uuid}',
                "tipo_fiscal": "SUPLENTE"
            }
        ],
        "lote": "4"
    }

    response = client.post('/unidades-contratos/', data=json.dumps(payload), content_type='application/json')
    result = json.loads(response.content)

    assert response.status_code == status.HTTP_201_CREATED
    assert ContratoUnidade.objects.get(uuid=result["uuid"]).fiscais.all().count() == 2


def test_fiscal_contrato_unidade_api_update(contrato_unidade, fake_user, client):
    payload = {
        "contrato": f'{contrato_unidade.contrato.uuid}',
        "unidade": f'{contrato_unidade.unidade.uuid}',
        "fiscais": [
            {
                "fiscal": f'{fake_user.uuid}',
                "tipo_fiscal": "TITULAR"
            },
            {
                "fiscal": f'{fake_user.uuid}',
                "tipo_fiscal": "SUPLENTE"
            }
        ],
        "lote": "4"
    }

    assert ContratoUnidade.objects.get(uuid=contrato_unidade.uuid).fiscais.all().count() == 0

    response = client.patch(f'/unidades-contratos/{contrato_unidade.uuid}/', data=json.dumps(payload),
                            content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    assert ContratoUnidade.objects.get(uuid=contrato_unidade.uuid).fiscais.all().count() == 2
