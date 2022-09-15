import pytest
from model_mommy import mommy

from ..api.serializers.produto_serializer import (
    ProdutoLookUpSerializer,
    ProdutoSerializer,
    ProdutoSimplesSerializer,
    UnidadeDeMedidaSerializer
)
from ..models.produto import Produto, UnidadeDeMedida

pytestmark = pytest.mark.django_db


@pytest.fixture
def unidade_medida():
    return mommy.make(UnidadeDeMedida, id=1, nome='Unidade Teste')


def test_unidade_medida_serializer(unidade_medida):
    unidadeMedida_serializer = UnidadeDeMedidaSerializer(unidade_medida)

    assert unidadeMedida_serializer.data is not None
    assert unidadeMedida_serializer.data['nome'] == 'Unidade Teste'
    assert unidadeMedida_serializer.data['uuid']


@pytest.fixture
def produto():
    return mommy.make(Produto, id=1, nome='Produto Teste')


def test_produto_serializer(produto):
    produto_serializer = ProdutoSerializer(produto)

    assert produto_serializer.data is not None
    assert 'id' not in produto_serializer.data
    assert produto_serializer.data['nome'] == 'PRODUTO TESTE'
    assert produto_serializer.data['uuid']


def test_produto_lookup_serializer(produto):
    produto_serializer = ProdutoLookUpSerializer(produto)

    assert produto_serializer.data is not None
    assert list(produto_serializer.data.keys()) == [
        'id',
        'uuid',
        'nome',
        'categoria',
        'grupo_alimentar',
        'tipo_programa'
    ]
    assert produto_serializer.data['nome'] == 'PRODUTO TESTE'


def test_produto_simples_serializer(produto):
    produto_serializer = ProdutoSimplesSerializer(produto)

    assert produto_serializer.data is not None
    assert list(produto_serializer.data.keys()) == [
        'uuid',
        'nome',
        'unidade_medida',
    ]
    assert produto_serializer.data['nome'] == 'PRODUTO TESTE'
