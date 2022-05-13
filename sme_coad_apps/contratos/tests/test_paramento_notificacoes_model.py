# TODO: Estado de contrato deixou de existeir. Necessário repensar o fluxo de notificação
# flake8: noqa
# import datetime
#
# import pytest
# from django.contrib import admin
# from freezegun import freeze_time
# from model_mommy import mommy
#
# from ..admin import ParametroNotificacoesVigenciaAdmin
# from ..models import Contrato, ParametroNotificacoesVigencia
#
# pytestmark = pytest.mark.django_db
#
#
# @pytest.fixture
# def parametro_notificacao():
#     return mommy.make(
#         'ParametroNotificacoesVigencia',
#         estado_contrato='teste',
#         vencendo_em=100,
#         repetir_notificacao_a_cada=7,
#     )
#
#
# @pytest.fixture
# def parametros_notificacao_por_estado():
#     mommy.make('ParametroNotificacoesVigencia', estado_contrato='teste', vencendo_em=90,
#                repetir_notificacao_a_cada=9)
#     mommy.make('ParametroNotificacoesVigencia', estado_contrato='teste', vencendo_em=100,
#                repetir_notificacao_a_cada=10)
#     mommy.make('ParametroNotificacoesVigencia', estado_contrato='teste', vencendo_em=50,
#                repetir_notificacao_a_cada=5)
#     mommy.make('ParametroNotificacoesVigencia', estado_contrato='teste', vencendo_em=200,
#                repetir_notificacao_a_cada=20)
#
#
# def test_instance_model(parametro_notificacao):
#     assert isinstance(parametro_notificacao, ParametroNotificacoesVigencia)
#     assert isinstance(parametro_notificacao.estado_contrato, str)
#     assert isinstance(parametro_notificacao.vencendo_em, int)
#     assert isinstance(parametro_notificacao.repetir_notificacao_a_cada, int)
#     assert parametro_notificacao.historico
#
#
# # def test_srt_model(parametro_notificacao):
# #     expected = (f'Contratos {Contrato.ESTADO_NOMES[parametro_notificacao.estado_contrato]} '
# #                 f'notificar a partir de {parametro_notificacao.vencendo_em} dias '
# #                 f'repetindo a cada {parametro_notificacao.repetir_notificacao_a_cada} dias.')
# #     assert parametro_notificacao.__str__() == expected
#
#
# def test_meta_modelo(parametro_notificacao):
#     assert parametro_notificacao._meta.verbose_name == 'Parâmetro de notificação de vigência'
#     assert parametro_notificacao._meta.verbose_name_plural == 'Parâmetros de notificação de vigência'
#
#
# def test_admin():
#     model_admin = ParametroNotificacoesVigenciaAdmin(ParametroNotificacoesVigencia, admin.site)
#     # pylint: disable=W0212
#     assert admin.site._registry[ParametroNotificacoesVigencia]
#     assert model_admin.list_display == ('vencendo_em', 'repetir_notificacao_a_cada')
#
#
# def test_parametros_do_estado_decrescente(parametros_notificacao_por_estado):
#     parametros_estado_emergencial = ParametroNotificacoesVigencia.parametros_do_estado('teste')
#
#     assert parametros_estado_emergencial.count() == 3
#     assert parametros_estado_emergencial.first().vencendo_em == 100
#     assert parametros_estado_emergencial.first().estado_contrato == Contrato.ESTADO_EMERGENCIAL
#
#
# def test_parametros_do_estado_crescente(parametros_notificacao_por_estado):
#     parametros_estado_emergencial = ParametroNotificacoesVigencia.parametros_do_estado(Contrato.ESTADO_EMERGENCIAL,
#                                                                                        crescente=True)
#
#     assert parametros_estado_emergencial.count() == 3
#     assert parametros_estado_emergencial.first().vencendo_em == 50
#     assert parametros_estado_emergencial.first().estado_contrato == Contrato.ESTADO_EMERGENCIAL
#
#
# @freeze_time('2019-01-01')
# def test_data_limite_do_estado(parametros_notificacao_por_estado):
#     data_limite_esperada = datetime.date(2019, 1, 1) + datetime.timedelta(days=100)
#     assert ParametroNotificacoesVigencia.data_limite_do_estado(Contrato.ESTADO_EMERGENCIAL) == data_limite_esperada
#
#
# def test_estado_notificavel(parametros_notificacao_por_estado):
#     # Se existem parâmetros para o estado, então ele é notificável
#     assert ParametroNotificacoesVigencia.estado_notificavel(Contrato.ESTADO_VIGENTE)
#
#     # Não existem parâmetros para o estado, então ele não é notificável
#     assert not ParametroNotificacoesVigencia.estado_notificavel(Contrato.ESTADO_EXCEPCIONAL)
#
#
# def test_get_frequencia_repeticao_por_dias_pra_vencer(parametros_notificacao_por_estado):
#     assert ParametroNotificacoesVigencia.frequencia_repeticao(estado=Contrato.ESTADO_EMERGENCIAL,
#                                                               dias_pra_vencer=55) == 9
