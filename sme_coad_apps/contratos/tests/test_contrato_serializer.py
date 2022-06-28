import datetime

import pytest
from model_mommy import mommy

from ...core.models import Nucleo
from ..api.serializers.contrato_serializer import ContratoLookUpSerializer, ContratoSerializer
from ..models.contrato import Contrato, Edital, Empresa, Objeto

pytestmark = pytest.mark.django_db


def test_contrato_serializer(fake_user):
    objeto = mommy.make(Objeto, id=1, nome='teste')
    empresa = mommy.make(Empresa, id=1, cnpj='55803656000134', nome='teste')
    contrato = mommy.make(
        Contrato,
        data_assinatura=datetime.date(2019, 10, 1),
        data_ordem_inicio=datetime.date(2019, 10, 1),
        objeto=objeto,
        empresa_contratada=empresa,
        vigencia=100,
        processo='12233',
        nucleo_responsavel=mommy.make(Nucleo),
        edital=mommy.make(Edital)
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
    assert contrato_serializer.data['vigencia'] is not None
    assert contrato_serializer.data['situacao']
    assert contrato_serializer.data['observacoes'] is not None
    assert contrato_serializer.data['nucleo_responsavel']
    assert contrato_serializer.data['edital']
    contrato_empresa_contratada = dict(contrato_serializer.data['empresa_contratada'])
    contrato_empresa_contratada.pop('alterado_em')
    contrato_empresa_contratada.pop('criado_em')
    resultado_esperado = {'contatos': [], 'cnpj': '55.803.656/0001-34',
                          'tipo_servico': {'id': 'ARMAZEM/DISTRIBUIDOR', 'nome': 'Armazém/Distribuidor'},
                          'tipo_fornecedor': {'id': '', 'nome': ''},
                          'situacao': {'id': 'ATIVA', 'nome': 'Ativa'},
                          'nome': empresa.nome,
                          'uuid': str(empresa.uuid), 'razao_social': '',
                          'cep': '', 'endereco': '', 'bairro': '', 'cidade': '', 'estado': '',
                          'numero': '', 'complemento': ''}
    assert contrato_empresa_contratada == resultado_esperado
    assert contrato_serializer.data['data_encerramento'] is not None
    assert contrato_serializer.data['objeto'] == {'nome': objeto.nome, 'uuid': str(objeto.uuid), 'id': objeto.id}
    assert contrato_serializer.data['total_mensal'] is not None
    assert contrato_serializer.data['row_index'] is not None
    assert contrato_serializer.data['dres'] is not None


def test_contrato_lookup_serializer(fake_user):
    contrato = mommy.make(
        Contrato,
        termo_contrato='00/00',
        criado_em=datetime.date(2019, 10, 1),
    )

    contrato_serializer = ContratoLookUpSerializer(contrato)

    assert contrato_serializer.data is not None
    assert contrato_serializer.data['termo_contrato'] == '00/00'
    assert contrato_serializer.data['uuid']
