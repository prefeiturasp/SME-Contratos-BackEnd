import pytest
from model_mommy import mommy

from ..api.serializers.tipo_servico_serializer import TipoServicoSerializer
from ..models.contrato import TipoServico

pytestmark = pytest.mark.django_db


def test_tipo_servico_serializer():
    tipo_servico = mommy.make(TipoServico, id=1, nome='teste')

    tipo_servico_serializer = TipoServicoSerializer(tipo_servico)

    assert tipo_servico_serializer.data is not None
    assert tipo_servico_serializer.data['id'] == 1
    assert tipo_servico_serializer.data['nome'] == 'teste'
