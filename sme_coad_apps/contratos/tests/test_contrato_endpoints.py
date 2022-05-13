import json

import pytest
from rest_framework import status

from ..models.contrato import Contrato

pytestmark = pytest.mark.django_db


def test_url_unauthorized(client):
    response = client.get('/contratos/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_url_authorized(authencticated_client):
    response = authencticated_client.get('/contratos/')
    assert response.status_code == status.HTTP_200_OK


def test_atualizacao_contrato(authencticated_client, contrato):
    data = {'termo_contrato': '129/14', 'tipo_servico': '7baa3356-599f-4627-9fed-832ee888de14',
            'processo': '6016.2017/0000791-6', 'situacao': 'ATIVO',
            'data_encerramento': '2019-12-12', 'data_assinatura': '2020-05-18', 'data_ordem_inicio': '2014-12-13',
            'vigencia': 1825,
            'dotacao_orcamentaria': ['2100 39', '16.24 2100 39'],
            'observacoes': '', 'objeto': '<p>dsadsad</p>',
            'numero_edital': '123123123',
            'unidades_selecionadas': [{'unidade': {'cd_equipamento': '108101',
                                                   'nm_exibicao_equipamento': 'ASSISTENCIA ADMINISTRATIVA-CE BT',
                                                   'nm_equipamento': 'ASSISTENCIA ADMINISTRATIVA-CE BT',
                                                   'cd_tp_equipamento': 3,
                                                   'dc_tp_equipamento': 'UNIDADE ADMINISTRATIVA', 'cd_tp_escola': None,
                                                   'dc_tipo_escola': None, 'sg_tp_escola': None, 'cd_tp_ua': 8,
                                                   'dc_tp_ua': 'OUTROS LOCAIS DA PMSP                             ',
                                                   'sg_tp_ua': 'OUT-PMSP ', 'cd_diretoria_referencia': '108100',
                                                   'nm_diretoria_referencia': 'DIRETORIA REGIONAL DE EDUCACAO BUTANTA',
                                                   'nm_exibicao_diretoria_referencia': 'DRE - BT',
                                                   'cd_diretoria_portal': '108100',
                                                   'nm_diretoria_portal': 'DIRETORIA REGIONAL DE EDUCACAO BUTANTA',
                                                   'nm_exibicao_diretoria_portal': 'DRE - BT', 'cd_logradouro': 1005,
                                                   'logradouro': 'RUA ALVARENGA, nº 573', 'bairro': 'BUTANTA',
                                                   'checked': True}, 'lote': '1', 'rf_fiscal': '1111111',
                                       'nome_fiscal': 'Galvão Bueno', 'suplentes': []}, {
                                          'unidade': {'cd_equipamento': '108102',
                                                      'nm_exibicao_equipamento': 'SUPERVISAO ESCOLAR - BT',
                                                      'nm_equipamento': 'SUPERVISAO ESCOLAR - BT',
                                                      'cd_tp_equipamento': 3,
                                                      'dc_tp_equipamento': 'UNIDADE ADMINISTRATIVA',
                                                      'cd_tp_escola': None, 'dc_tipo_escola': None,
                                                      'sg_tp_escola': None, 'cd_tp_ua': 8,
                                                      'dc_tp_ua': 'OUTROS LOCAIS DA PMSP                             ',
                                                      'sg_tp_ua': 'OUT-PMSP ', 'cd_diretoria_referencia': '108100',
                                                      'nm_diretoria_referencia': 'DIRETORIA REGIONAL DE EDUCACAO BUTANTA',  # noqa E501
                                                      'nm_exibicao_diretoria_referencia': 'DRE - BT',
                                                      'cd_diretoria_portal': '108100',
                                                      'nm_diretoria_portal': 'DIRETORIA REGIONAL DE EDUCACAO BUTANTA',
                                                      'nm_exibicao_diretoria_portal': 'DRE - BT', 'cd_logradouro': 1004,
                                                      'logradouro': 'RUA AZEM ABDALA AZEM, nº 564',
                                                      'bairro': 'JARDIM BONFIGLIOLI', 'checked': True}, 'lote': '1',
                                          'rf_fiscal': '1111111', 'nome_fiscal': 'Galvão Bueno', 'suplentes': []}, {
                                          'unidade': {'cd_equipamento': '200184',
                                                      'nm_exibicao_equipamento': 'ARICANDUVA - PROFESSORA IRENE GALVAO DE SOUZA',  # noqa E501
                                                      'nm_equipamento': 'ARICANDUVA - PROFESSORA IRENE GALVAO DE SOUZA',
                                                      'cd_tp_equipamento': 3,
                                                      'dc_tp_equipamento': 'UNIDADE ADMINISTRATIVA',
                                                      'cd_tp_escola': None, 'dc_tipo_escola': None,
                                                      'sg_tp_escola': None, 'cd_tp_ua': 19,
                                                      'dc_tp_ua': 'CENTRO EDUCACIONAL UNIFICADO                      ',
                                                      'sg_tp_ua': 'CEU      ', 'cd_diretoria_referencia': '108700',
                                                      'nm_diretoria_referencia': 'DIRETORIA REGIONAL DE EDUCACAO ITAQUERA', # noqa E501
                                                      'nm_exibicao_diretoria_referencia': 'DRE - IQ',
                                                      'cd_diretoria_portal': '108700',
                                                      'nm_diretoria_portal': 'DIRETORIA REGIONAL DE EDUCACAO ITAQUERA',
                                                      'nm_exibicao_diretoria_portal': 'DRE - IQ', 'cd_logradouro': 93,
                                                      'logradouro': 'RUA OLGA FADEL ABARCA, nº S/N',
                                                      'bairro': 'JARDIM SANTA TEREZINHA ZONA LESTE', 'checked': True},
                                          'lote': '2', 'rf_fiscal': '1234567', 'nome_fiscal': 'Calvin Feitosa',
                                          'suplentes': [{'nome': 'Galvão Bueno', 'rf': '1111111'}]}, {
                                          'unidade': {'cd_equipamento': '200186',
                                                      'nm_exibicao_equipamento': 'CIDADE DUTRA',
                                                      'nm_equipamento': 'CIDADE DUTRA - ADIB SALOMAO, DR ',
                                                      'cd_tp_equipamento': 3,
                                                      'dc_tp_equipamento': 'UNIDADE ADMINISTRATIVA',
                                                      'cd_tp_escola': None, 'dc_tipo_escola': None,
                                                      'sg_tp_escola': None, 'cd_tp_ua': 19,
                                                      'dc_tp_ua': 'CENTRO EDUCACIONAL UNIFICADO                      ',
                                                      'sg_tp_ua': 'CEU      ', 'cd_diretoria_referencia': '108300',
                                                      'nm_diretoria_referencia': 'DIRETORIA REGIONAL DE EDUCACAO CAPELA DO SOCORRO',  # noqa E501
                                                      'nm_exibicao_diretoria_referencia': 'DRE - CS',
                                                      'cd_diretoria_portal': '108300',
                                                      'nm_diretoria_portal': 'DIRETORIA REGIONAL DE EDUCACAO CAPELA DO SOCORRO',  # noqa E501
                                                      'nm_exibicao_diretoria_portal': 'DRE - CS', 'cd_logradouro': 171,
                                                      'logradouro': 'AVENIDA INTERLAGOS, nº 7350',
                                                      'bairro': 'INTERLAGOS', 'checked': True}, 'lote': '2',
                                          'rf_fiscal': '1234567', 'nome_fiscal': 'Calvin Feitosa',
                                          'suplentes': [{'nome': 'Galvão Bueno', 'rf': '1111111'}]}, {
                                          'unidade': {'cd_equipamento': '013358',
                                                      'nm_exibicao_equipamento': 'EMEI PRES. JANIO QUADROS',
                                                      'nm_equipamento': 'EMEI JANIO QUADROS, PRES.',
                                                      'cd_tp_equipamento': 1, 'dc_tp_equipamento': 'ESCOLA',
                                                      'cd_tp_escola': 2,
                                                      'dc_tipo_escola': 'ESCOLA MUNICIPAL DE EDUCACAO INFANTIL',
                                                      'sg_tp_escola': 'EMEI', 'cd_tp_ua': None, 'dc_tp_ua': None,
                                                      'sg_tp_ua': None, 'cd_diretoria_referencia': '108800',
                                                      'nm_diretoria_referencia': 'DIRETORIA REGIONAL DE EDUCACAO JACANA/TREMEMBE',  # noqa E501
                                                      'nm_exibicao_diretoria_referencia': 'DRE - JT',
                                                      'cd_diretoria_portal': '108800',
                                                      'nm_diretoria_portal': 'DIRETORIA REGIONAL DE EDUCACAO JACANA/TREMEMBE',  # noqa E501
                                                      'nm_exibicao_diretoria_portal': 'DRE - JT', 'cd_logradouro': 3142,
                                                      'logradouro': 'RUA CANTO DO ENGENHO, nº 240',
                                                      'bairro': 'PARQUE CASA DE PEDRA', 'checked': True}, 'lote': '3',
                                          'rf_fiscal': '1234567', 'nome_fiscal': 'Calvin Feitosa', 'suplentes': []}, {
                                          'unidade': {'cd_equipamento': '019214',
                                                      'nm_exibicao_equipamento': 'CEU EMEI JD VL NOVA',
                                                      'nm_equipamento': 'CEU EMEI JARDIM VILA NOVA',
                                                      'cd_tp_equipamento': 1, 'dc_tp_equipamento': 'ESCOLA',
                                                      'cd_tp_escola': 17,
                                                      'dc_tipo_escola': 'CENTRO EDUCACIONAL UNIFICADO - EMEI',
                                                      'sg_tp_escola': 'CEU EMEI', 'cd_tp_ua': None, 'dc_tp_ua': None,
                                                      'sg_tp_ua': None, 'cd_diretoria_referencia': '108700',
                                                      'nm_diretoria_referencia': 'DIRETORIA REGIONAL DE EDUCACAO ITAQUERA',  # noqa E501
                                                      'nm_exibicao_diretoria_referencia': 'DRE - IQ',
                                                      'cd_diretoria_portal': '108700',
                                                      'nm_diretoria_portal': 'DIRETORIA REGIONAL DE EDUCACAO ITAQUERA',
                                                      'nm_exibicao_diretoria_portal': 'DRE - IQ', 'cd_logradouro': 373,
                                                      'logradouro': 'AVENIDA ERNESTO SOUZA CRUZ, nº 2171',
                                                      'bairro': 'CIDADE ANTÔNIO ESTEVÃO DE CARVALHO', 'checked': True},
                                          'lote': '3', 'rf_fiscal': '1234567', 'nome_fiscal': 'Calvin Feitosa',
                                          'suplentes': []}]}
    response = authencticated_client.put(f'/contratos/{contrato.uuid}/', content_type='application/json', data=data)
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json.get('lotes')) == 3


def test_url_situacoes(authencticated_client):
    response = authencticated_client.get('/contratos/situacoes/')
    assert response.status_code == status.HTTP_200_OK
    json_data = json.loads(response.content)
    assert json_data == Contrato.situacoes_to_json()
