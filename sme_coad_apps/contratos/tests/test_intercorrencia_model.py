import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import IntercorrenciaAdmin
from ..models import Contrato, Intercorrencia

pytestmark = pytest.mark.django_db


def test_instance_model(intercorrencia):
    assert isinstance(intercorrencia, Intercorrencia)
    assert isinstance(intercorrencia.contrato, Contrato)
    assert isinstance(intercorrencia.tipo_intercorrencia, str)
    assert isinstance(intercorrencia.data_inicial, datetime.date)
    assert isinstance(intercorrencia.data_final, datetime.date)
    assert isinstance(intercorrencia.acrescentar_dias, bool)
    assert isinstance(intercorrencia.motivo_suspensao, str)
    assert isinstance(intercorrencia.opcao_suspensao, str)
    assert isinstance(intercorrencia.descricao_suspensao, str)


def test_tipos_suspensao_intercorrencia():
    assert Intercorrencia.TIPO_INTERCORRENCIA_SUSPENSAO
    assert Intercorrencia.TIPO_INTERCORRENCIA_IMPEDIMENTO
    assert Intercorrencia.TIPO_INTERCORRENCIA_RESCISAO


def test_motivos_suspensao_intercorrencia():
    assert Intercorrencia.MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA
    assert Intercorrencia.MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO
    assert Intercorrencia.MOTIVO_SUSPENSAO_CONSENSUALMENTE


def test_srt_model():
    model = mommy.make('Intercorrencia', tipo_intercorrencia=Intercorrencia.TIPO_INTERCORRENCIA_SUSPENSAO)
    assert model.__str__() == 'SUSPENSAO'


def test_meta_modelo():
    model = mommy.make('Intercorrencia')
    assert model._meta.verbose_name == 'Intercorrência'
    assert model._meta.verbose_name_plural == 'Intercorrências'


def test_admin():
    model_admin = IntercorrenciaAdmin(Intercorrencia, admin.site)
    assert admin.site._registry[Intercorrencia]
    assert model_admin.list_display == ('tipo_intercorrencia', 'contrato', 'data_inicial', 'data_final',
                                        'motivo_suspensao', 'opcao_suspensao', 'descricao_suspensao')
    assert model_admin.search_fields == ('tipo_intercorrencia', 'contrato')
