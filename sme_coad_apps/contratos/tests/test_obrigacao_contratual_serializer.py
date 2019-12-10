import pytest
from model_mommy import mommy

from ..api.serializers.obrigacao_contratual_serializer import ObrigacaoContratualSerializer

pytestmark = pytest.mark.django_db


def test_obrigacao_contratual_serializer():
    contrato = mommy.make('Contrato')
    obrigacao_contratual = mommy.make('ObrigacaoContratual', contrato=contrato, item='01', obrigacao='teste')

    serializer = ObrigacaoContratualSerializer(obrigacao_contratual)

    assert serializer.data is not None
    assert serializer.data['contrato']
    assert serializer.data['item']
    assert serializer.data['obrigacao']
