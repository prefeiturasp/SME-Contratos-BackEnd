import json

import pytest

pytestmark = pytest.mark.django_db


def test_get_produto_filters(authencticated_client, produto):
    rota = f"""/produtos/?nome={produto.nome}
                    &situacao=ATIVO
                    &categoria=ALIMENTO
                    &durabilidade=NAO_PERECIVEL
                    &armazenabilidade=ARMAZENAVEL
                    &grupo_alimentar=SECOS"""

    url = rota.replace('\n', '')
    response = authencticated_client.get(url, content_type='application/json')
    resposta = json.loads(response.content)
    esperado = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'uuid': str(produto.uuid),
                'nome': produto.nome,
                'id': produto.id,
                'categoria': 'Alimento',
                'durabilidade': 'Não perecível',
                'grupo_alimentar': 'Secos',
                'armazenabilidade': 'Armazenável'
            }
        ]
    }
    assert resposta == esperado
