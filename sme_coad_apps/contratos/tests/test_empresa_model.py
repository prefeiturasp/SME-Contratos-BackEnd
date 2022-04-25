import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import EmpresaAdmin
from ..models import Empresa

pytestmark = pytest.mark.django_db


def test_instance_model():
    model = mommy.make('Empresa', nome='Teste LTDA')
    assert isinstance(model, Empresa)
    assert isinstance(model.nome, str)
    assert isinstance(model.cnpj, str)
    assert isinstance(model.razao_social, str)
    assert isinstance(model.tipo_servico, str)
    assert isinstance(model.tipo_fornecedor, str)
    assert isinstance(model.situacao, str)
    assert isinstance(model.cep, str)
    assert isinstance(model.endereco, str)
    assert isinstance(model.bairro, str)
    assert isinstance(model.cidade, str)
    assert isinstance(model.estado, str)
    assert isinstance(model.numero, str)
    assert isinstance(model.complemento, str)
    assert model.historico


def test_srt_model():
    model = mommy.make('Empresa', nome='Teste LTDA')
    assert model.__str__() == 'Teste LTDA'


def test_meta_modelo():
    model = mommy.make('Empresa')
    assert model._meta.verbose_name == 'Empresa'
    assert model._meta.verbose_name_plural == 'Empresas'


def test_admin():
    model_admin = EmpresaAdmin(Empresa, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Empresa]
    assert model_admin.list_display == ('nome', 'get_cnpj_formatado')
    assert model_admin.ordering == ('nome',)
    assert model_admin.search_fields == ('nome', 'cnpj')
