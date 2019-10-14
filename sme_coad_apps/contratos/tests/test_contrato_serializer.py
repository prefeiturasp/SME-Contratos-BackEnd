import datetime

import pytest
from model_mommy import mommy

from ..api.serializers.contrato_serializer import ContratoSerializer
from ..models.contrato import Contrato, TipoServico, Empresa

pytestmark = pytest.mark.django_db


def test_contrato_serializer(fake_user):
    tipo_servico = mommy.make(TipoServico, id=1, nome='teste')
    empresa = mommy.make(Empresa, id=1, cnpj='55803656000134', nome='teste')
    contrato = mommy.make(
        Contrato,
        data_assinatura=datetime.date(2019, 10, 1),
        data_ordem_inicio=datetime.date(2019, 10, 1),
        gestor=fake_user,
        tipo_servico=tipo_servico,
        empresa_contratada=empresa,
        vigencia_em_dias=100,
    )

    contrato_serializer = ContratoSerializer(contrato)

    assert contrato_serializer.data is not None
    assert contrato_serializer.data['termo_contrato']
    assert contrato_serializer.data['criado_em']
    assert contrato_serializer.data['alterado_em']
    assert contrato_serializer.data['uuid']
    assert contrato_serializer.data['processo']
    assert contrato_serializer.data['data_assinatura']
    assert contrato_serializer.data['data_ordem_inicio']
    assert contrato_serializer.data['vigencia_em_dias'] is not None
    assert contrato_serializer.data['situacao']
    assert contrato_serializer.data['observacoes'] is not None
    assert contrato_serializer.data['estado_contrato']
    assert contrato_serializer.data['nucleo_responsavel']
    assert contrato_serializer.data['empresa_contratada'] == {'nome': empresa.nome, 'uuid': str(empresa.uuid)}
    assert contrato_serializer.data['gestor'] == {'nome': fake_user.nome, 'uuid': str(fake_user.uuid)}
    assert contrato_serializer.data['data_encerramento'] is not None
    assert contrato_serializer.data['tipo_servico'] == {'nome': tipo_servico.nome, 'uuid': str(tipo_servico.uuid)}
    assert contrato_serializer.data['total_mensal'] is not None
