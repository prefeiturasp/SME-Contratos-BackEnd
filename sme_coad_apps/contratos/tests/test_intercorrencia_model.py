import datetime

import pytest
from django.contrib import admin
from model_mommy import mommy

from ..admin import ImpedimentoAdmin, RescisaoAdmin, SuspensaoAdmin
from ..models import Contrato, Impedimento, Intercorrencia, Rescisao, Suspensao

pytestmark = pytest.mark.django_db


def test_tipos_intercorrencia():
    assert Intercorrencia.TIPO_INTERCORRENCIA_SUSPENSAO
    assert Intercorrencia.TIPO_INTERCORRENCIA_IMPEDIMENTO
    assert Intercorrencia.TIPO_INTERCORRENCIA_RESCISAO


def test_instance_model_impedimento(impedimento):
    assert isinstance(impedimento, Impedimento)
    assert isinstance(impedimento.contrato, Contrato)
    assert isinstance(impedimento.tipo_intercorrencia, str)
    assert isinstance(impedimento.data_inicial, datetime.date)
    assert isinstance(impedimento.data_final, datetime.date)
    assert isinstance(impedimento.descricao_impedimento, str)


def test_srt_model_impedimento():
    model = mommy.make('Impedimento', tipo_intercorrencia=Impedimento.TIPO_INTERCORRENCIA_IMPEDIMENTO)
    assert model.__str__() == 'IMPEDIMENTO'


def test_meta_modelo_impedimento():
    model = mommy.make('Impedimento')
    assert model._meta.verbose_name == 'Impedimento'
    assert model._meta.verbose_name_plural == 'Impedimentos'


def test_admin_impedimento():
    model_admin = ImpedimentoAdmin(Impedimento, admin.site)
    assert admin.site._registry[Impedimento]
    assert model_admin.list_display == ('tipo_intercorrencia', 'contrato', 'data_inicial', 'data_final',
                                        'descricao_impedimento', 'anexo')
    assert model_admin.search_fields == ('tipo_intercorrencia', 'contrato')


def test_instance_model_rescisao(rescisao):
    assert isinstance(rescisao, Rescisao)
    assert isinstance(rescisao.contrato, Contrato)
    assert isinstance(rescisao.tipo_intercorrencia, str)
    assert isinstance(rescisao.data_rescisao, datetime.date)
    assert isinstance(rescisao.motivo_rescisao, list)


def test_motivos_rescisao_intercorrencia():
    assert Rescisao.MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS
    assert Rescisao.MOTIVO_RESCISAO_CUMPRIMENTO_IRREGULAR
    assert Rescisao.MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO
    assert Rescisao.MOTIVO_RESCISAO_ATRASO_INJUSTIFICADO
    assert Rescisao.MOTIVO_RESCISAO_PARALISACAO_DO_SERVICO
    assert Rescisao.MOTIVO_RESCISAO_SUBCONTRATACAO_DO_OBJETO
    assert Rescisao.MOTIVO_RESCISAO_DESATENDIMENTO_DAS_DETERMINACOES
    assert Rescisao.MOTIVO_RESCISAO_COMENTIMENTO_DE_FALTAS
    assert Rescisao.MOTIVO_RESCISAO_DECRETACAO_DE_FALENCIA
    assert Rescisao.MOTIVO_RESCISAO_DISSOLUCAO_OU_FALENCIMENTO
    assert Rescisao.MOTIVO_RESCISAO_ALTERACAO_DE_FINALIDADE
    assert Rescisao.MOTIVO_RESCISAO_INTERESSE_PUBLICO
    assert Rescisao.MOTIVO_RESCISAO_SUPRESSAO_DA_ADMINISTACAO
    assert Rescisao.MOTIVO_RESCISAO_SUSPENSAO_DA_EXECUCAO
    assert Rescisao.MOTIVO_RESCISAO_ATRASO_DOS_PAGAMENTOS
    assert Rescisao.MOTIVO_RESCISAO_NAO_LIBERACAO_ADMINISTRACAO
    assert Rescisao.MOTIVO_RESCISAO_OCORRENCIA_CASO_FORTUITO
    assert Rescisao.MOTIVO_RESCISAO_DESCUPRIMENTO_DA_LEI


def test_srt_model_rescisao():
    model = mommy.make('Rescisao', tipo_intercorrencia=Rescisao.TIPO_INTERCORRENCIA_RESCISAO)
    assert model.__str__() == 'RESCISAO'


def test_meta_modelo_rescisao():
    model = mommy.make('Rescisao')
    assert model._meta.verbose_name == 'Rescisão'
    assert model._meta.verbose_name_plural == 'Rescisões'


def test_admin_rescisao():
    model_admin = RescisaoAdmin(Rescisao, admin.site)
    assert admin.site._registry[Rescisao]
    assert model_admin.list_display == ('tipo_intercorrencia', 'contrato', 'data_rescisao', 'motivo_rescisao')
    assert model_admin.search_fields == ('tipo_intercorrencia', 'contrato')


def test_instance_model_suspensao(suspensao):
    assert isinstance(suspensao, Suspensao)
    assert isinstance(suspensao.contrato, Contrato)
    assert isinstance(suspensao.tipo_intercorrencia, str)
    assert isinstance(suspensao.data_inicial, datetime.date)
    assert isinstance(suspensao.data_final, datetime.date)
    assert isinstance(suspensao.acrescentar_dias, bool)
    assert isinstance(suspensao.motivo_suspensao, str)
    assert isinstance(suspensao.opcao_suspensao, str)
    assert isinstance(suspensao.descricao_suspensao, str)


def test_motivos_suspensao_intercorrencia():
    assert Suspensao.MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA
    assert Suspensao.MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO
    assert Suspensao.MOTIVO_SUSPENSAO_CONSENSUALMENTE


def test_srt_model_suspensao():
    model = mommy.make('Suspensao', tipo_intercorrencia=Suspensao.TIPO_INTERCORRENCIA_SUSPENSAO)
    assert model.__str__() == 'SUSPENSAO'


def test_meta_modelo_suspensao():
    model = mommy.make('Suspensao')
    assert model._meta.verbose_name == 'Suspensão'
    assert model._meta.verbose_name_plural == 'Suspensões'


def test_admin_suspensao():
    model_admin = SuspensaoAdmin(Suspensao, admin.site)
    assert admin.site._registry[Suspensao]
    assert model_admin.list_display == ('tipo_intercorrencia', 'contrato', 'data_inicial', 'data_final',
                                        'motivo_suspensao', 'opcao_suspensao', 'descricao_suspensao')
    assert model_admin.search_fields == ('tipo_intercorrencia', 'contrato')
