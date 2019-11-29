import pytest
from model_mommy import mommy

from ..api.serializers.modelo_ateste_serializer import ModeloAtesteSerializer

pytestmark = pytest.mark.django_db


def test_modelo_ateste_serializer():
    modelo_ateste = mommy.make('ModeloAteste', titulo='teste')

    serializer = ModeloAtesteSerializer(modelo_ateste)

    assert serializer.data is not None
    assert serializer.data['titulo']
