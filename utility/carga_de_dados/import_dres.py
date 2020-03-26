import json

import environ

from sme_coad_apps.core.models import Unidade

ROOT_DIR = environ.Path(__file__) - 1


def update_or_create_dre(unidade_data: dict):
    try:
        dre = Unidade.objects.get(codigo_eol=unidade_data['codigo_eol'])
        dre.nome = unidade_data['nome']
        dre.sigla = unidade_data['sigla']
        dre.cep = unidade_data['cep']
        dre.tipo_unidade = 'DRE'
        dre.equipamento = 'UA'
        dre.save()
        print(f"Atualizada Unidade {unidade_data['nome']}")
    except Unidade.DoesNotExist:
        dre = Unidade.objects.create(**unidade_data)
        print(f"Criada Unidade {unidade_data['nome']}")

    return dre


def update_dre_unidade(codigo_eol_unidade, codigo_eol_dre):
    try:
        dre = Unidade.objects.get(codigo_eol=codigo_eol_dre)
    except Unidade.DoesNotExist:
        dre = None

    try:
        unidade = Unidade.objects.get(codigo_eol=codigo_eol_unidade)
        unidade.dre = dre
        unidade.save()
        print(f'Atualizada DRE. Unidade:{unidade.nome} DRE:{unidade.dre.sigla}')
    except Unidade.DoesNotExist:
        ...


def importa_dres():
    with open(f'{ROOT_DIR}/dres.json', 'r') as dresfile:
        data = dresfile.read()
        obj = json.loads(data)
        dres = obj['results']

    # Rodada 1
    # Percorre o json e para cada dre
    for dre in dres:
        # Procura a DRE e atualiza nome e sigla
        dre_data = {
            'equipamento': 'UA',
            'tipo_unidade': 'DRE',
            'codigo_eol': dre["cod_dre"],
            'cep': dre["cd_cep"],
            'dre': None,
            'sigla': dre["sg_dre"][-2:].strip(),
            'nome': dre["dre"],
        }
        print(f'DRE: {dre_data["codigo_eol"]} {dre_data["nome"]} Sigla:{dre_data["sigla"]}')
        update_or_create_dre(dre_data)

    # Rodada 2
    # Percorre o json e para cada dre
    for dre in dres:
        escolas = dre['escolas'].split(",")
        for codigo_eol in escolas:
            # Procura Unidade e atualiza a DRE
            print(f'Atualizar dre em {codigo_eol}')
            update_dre_unidade(codigo_eol, dre['cod_dre'])
