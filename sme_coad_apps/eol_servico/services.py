import environ
import requests
from rest_framework import status

env = environ.Env()
DJANGO_EOL_API_TOKEN = f'{env("DJANGO_EOL_API_TOKEN")}'
DJANGO_EOL_API_URL = f'{env("DJANGO_EOL_API_URL")}'


class EOLException(Exception):
    pass


class EOLService:
    HEADER = {
        'x-api-eol-key': f'{DJANGO_EOL_API_TOKEN}'
    }
    TIMEOUT = 20

    @classmethod
    def buscar_equipamentos(cls, codigo_subprefeitura=None, codigo_dre=None, tipo_escola=None):
        """Retorna dados do equipamento.

        Exemplo de retorno:
        [
            {
                "cd_equipamento": "00000",
                "nm_exibicao_equipamento": " XXXXXX",
                "nm_equipamento": " XXXXX",
                "cd_tp_equipamento": 0,
                "dc_tp_equipamento": "UNIDADE ADMINISTRATIVA",
                "cd_tp_escola": 0,
                "dc_tipo_escola": "",
                "sg_tp_escola": "",
                "cd_diretoria_referencia": "00000",
                "nm_diretoria_referencia": "XXXXXXXX",
                "nm_exibicao_diretoria_referencia": "XXXXXXXXX",
                "cd_diretoria_portal": "0000000",
                "nm_diretoria_portal": "XXXXXXXXX",
                "nm_exibicao_diretoria_portal": "XXXXXXXXX",
                "cd_logradouro": 0000,
                "logradouro": "XXX XXXXXXXXX Nº 3752",
                "bairro": "XXXXX XX XXX",
                "codigoSubprefeitura": "00",
                "nomeSubprefeitura": "XXXXXXXXXX",
                "ehCeu": true
            },
        ]
        """
        response = requests.get(f'{DJANGO_EOL_API_URL}/escolas/equipamentos',
                                headers=cls.HEADER, timeout=cls.TIMEOUT,
                                params={'CodigosSubprefeitura': codigo_subprefeitura, 'CodigosDre': codigo_dre,
                                        'TiposEscola': tipo_escola})

        if response.status_code == status.HTTP_200_OK:
            resultado = response.json()
            return resultado
        else:
            raise EOLException(f'Erro: {str(response)}, Status: {response.status_code}')
