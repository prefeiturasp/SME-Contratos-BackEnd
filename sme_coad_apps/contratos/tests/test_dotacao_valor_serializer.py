import pytest
from model_mommy import mommy

from ..api.serializers.dotacao_valor_serializer import DotacaoValorSerializer

pytestmark = pytest.mark.django_db


def test_dotacao_valor_serializer(dotacao_orcamentaria):
    contrato = mommy.make('Contrato')
    dotacao_valor = mommy.make(
        'DotacaoValor', contrato=contrato, dotacao_orcamentaria=dotacao_orcamentaria, valor='2000')

    serializer = DotacaoValorSerializer(dotacao_valor)

    assert serializer.data is not None
    assert serializer.data['dotacao_orcamentaria']
    assert serializer.data['valor']
