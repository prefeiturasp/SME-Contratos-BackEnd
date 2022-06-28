import environ
import requests
from rest_framework import status

env = environ.Env()

API_SOFI_URL = env('DJANGO_SOFI_API_URL', default=None)
SOFI_TOKEN = f'{env("DJANGO_SOFI_API_TOKEN")}'


class SOFIException(Exception):
    pass


class SOFIService(object):
    DEFAULT_HEADERS = {'Authorization': f'Bearer {SOFI_TOKEN}'}
    DEFAULT_TIMEOUT = 60

    @classmethod
    def get_informacoes_despesas(cls, ano_dotacao, mes_dotacao):
        try:
            response = requests.get(f'{API_SOFI_URL}/despesas?anoDotacao={ano_dotacao}&mesDotacao={mes_dotacao}',
                                    headers=cls.DEFAULT_HEADERS, timeout=cls.DEFAULT_TIMEOUT)
            if response.status_code == status.HTTP_200_OK:
                results = response.json()['lstDespesas']
                return results
            else:
                return False
        except requests.exceptions.Timeout:
            return False

    @classmethod
    def get_informacoes_empenhos(cls, ano_empenho, mes_empenho):
        try:
            response1 = requests.get(f'{API_SOFI_URL}/empenhos?anoEmpenho={ano_empenho}&mesEmpenho={mes_empenho}',
                                     headers=cls.DEFAULT_HEADERS, timeout=cls.DEFAULT_TIMEOUT)
            metadados = response1.json()['metadados']
            ultima_pagina = metadados.get('qtdPaginas', None)

            response = requests.get(
                f'{API_SOFI_URL}/empenhos?anoEmpenho={ano_empenho}&mesEmpenho={mes_empenho}&numPagina={ultima_pagina}',
                headers=cls.DEFAULT_HEADERS,
                timeout=cls.DEFAULT_TIMEOUT)
            if response.status_code == status.HTTP_200_OK:
                results = response.json()['lstEmpenhos']
                return results
            else:
                return False
        except requests.exceptions.Timeout:
            return False

    @classmethod
    def get_informacoes_contratos(cls, ano_contrato):
        try:
            response1 = requests.get(f'{API_SOFI_URL}/contratos?anoContrato={ano_contrato}',
                                     headers=cls.DEFAULT_HEADERS, timeout=cls.DEFAULT_TIMEOUT)
            metadados = response1.json()['metadados']
            ultima_pagina = metadados.get('qtdPaginas', None)

            response = requests.get(f'{API_SOFI_URL}/contratos?anoContrato={ano_contrato}&numPagina={ultima_pagina}',
                                    headers=cls.DEFAULT_HEADERS, timeout=cls.DEFAULT_TIMEOUT)
            if response.status_code == status.HTTP_200_OK:

                results = response.json()['lstContratos']
                return results
            else:
                return False
        except requests.exceptions.Timeout:
            return False

    @classmethod
    def get_informacoes_dispesas_por_credor(cls, ano_exercicio, mes_empenho):
        try:
            response = requests.get(
                f'{API_SOFI_URL}/despesasCredor?anoExercicio={ano_exercicio}&mesEmpenho={mes_empenho}',
                headers=cls.DEFAULT_HEADERS, timeout=cls.DEFAULT_TIMEOUT)
            if response.status_code == status.HTTP_200_OK:
                results = response.json()['lstDespesaCredores']
                return results
            else:
                return False
        except requests.exceptions.Timeout:
            return False
