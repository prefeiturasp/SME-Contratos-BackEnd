import json

import pytest

pytestmark = pytest.mark.django_db


def test_get_ata_filters(authencticated_client, empresa):
    rota = f"""/empresas/?nome={empresa.nome}
                &situacao=ATIVA
                &cnpj_empresa={empresa.cnpj}
                &tipo_servico=FORNECEDOR
                &tipo_fornecedor=CONVENCIONAL"""

    url = rota.replace('\n', '').replace(' ', '')
    response = authencticated_client.get(url, content_type='application/json')
    resposta = json.loads(response.content)
    esperado = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'uuid': str(empresa.uuid),
                'nome': empresa.nome,
                'id': empresa.id,
                'cnpj': '21.256.564/0001-60',
                'situacao': 'Ativa',
                'tipo_servico': 'Fornecedor'
            }
        ]
    }
    assert resposta == esperado
