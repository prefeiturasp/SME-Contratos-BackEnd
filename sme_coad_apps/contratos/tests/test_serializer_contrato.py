import datetime

import pytest
from model_mommy import mommy

from ..api.serializers.contrato_serializer import ContratoSerializer
from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_contrato_serializer(fake_user):
    contrato = mommy.make(
        Contrato,
        data_assinatura=datetime.date(2019, 10, 1),
        data_ordem_inicio=datetime.date(2019, 10, 1),
        gestor=fake_user
    )

    employee_serializer = ContratoSerializer(contrato)

    assert employee_serializer.data is not None
    assert employee_serializer.data['termo_contrato']
    assert employee_serializer.data['criado_em']
    assert employee_serializer.data['alterado_em']
    assert employee_serializer.data['uuid']
    assert employee_serializer.data['processo']
    assert employee_serializer.data['data_assinatura']
    assert employee_serializer.data['data_ordem_inicio']
    assert employee_serializer.data['vigencia_em_dias'] is not None
    assert employee_serializer.data['situacao']
    assert employee_serializer.data['observacoes'] is not None
    assert employee_serializer.data['estado_contrato']
    assert employee_serializer.data['tipo_servico']
    assert employee_serializer.data['nucleo_responsavel']
    assert employee_serializer.data['empresa_contratada']
    assert employee_serializer.data['gestor']
