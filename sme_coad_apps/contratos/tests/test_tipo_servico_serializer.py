import pytest
from model_mommy import mommy

from ..api.serializers.tipo_servico_serializer import TipoServicoSerializer, TipoServicoLookupSerializer
from ..models.contrato import TipoServico

pytestmark = pytest.mark.django_db


def test_tipo_servico_serializer():
    tipo_servico = mommy.make(TipoServico, id=1, nome='teste')

    tipo_servico_serializer = TipoServicoSerializer(tipo_servico)

    assert tipo_servico_serializer.data is not None
    assert 'id' not in tipo_servico_serializer.data
    assert tipo_servico_serializer.data['nome'] == 'teste'
    assert tipo_servico_serializer.data['uuid']


def test_tipo_servico_lookup_serializer():
    tipo_servico = mommy.make(TipoServico, id=1, nome='teste')

    tipo_servico_serializer = TipoServicoLookupSerializer(tipo_servico)

    assert tipo_servico_serializer.data is not None
    # TODO Remover id do serializer
    # assert 'id' not in tipo_servico_serializer.data
    assert tipo_servico_serializer.data['id']
    assert tipo_servico_serializer.data['nome'] == 'teste'
    assert tipo_servico_serializer.data['uuid']
