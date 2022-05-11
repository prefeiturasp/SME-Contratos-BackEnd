import pytest

from ..api.serializers.dotacao_valor_serializer import (
    DotacaoOrcamentariaLookUpSerializer,
    DotacaoOrcamentariaSerializer
)

pytestmark = pytest.mark.django_db


def test_dotacao_orcamentaria_serializer(dotacao_orcamentaria):
    serializer = DotacaoOrcamentariaSerializer(dotacao_orcamentaria)

    assert serializer.data is not None
    assert serializer.data['orgao']
    assert serializer.data['unidade']
    assert serializer.data['funcao']
    assert serializer.data['subfuncao']
    assert serializer.data['programa']
    assert serializer.data['projeto_atividade']
    assert serializer.data['conta_despesa']
    assert serializer.data['fonte']


def test_dotacao_orcamentaria_lookup_serializer(dotacao_orcamentaria):
    serializer = DotacaoOrcamentariaLookUpSerializer(dotacao_orcamentaria)

    assert serializer.data is not None
    assert serializer.data['uuid']
    assert serializer.data['numero_dotacao']
