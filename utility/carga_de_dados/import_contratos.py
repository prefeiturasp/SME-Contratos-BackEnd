import environ
import pandas as pd
from brazilnum.cnpj import clean_id

from sme_coad_apps.contratos.models import Empresa

ROOT_DIR = environ.Path(__file__) - 1

df = pd.read_excel(f'{ROOT_DIR}/contratos.xlsx',
                   converters={'TC': str,
                               'PROCESSO': str,
                               'CNPJ': str,
                               'LOTE': str,
                               'EOL_UNIDADE': str,
                               'CEP_UNIDADE': str,
                               'DOTACAO': str
                               },
                   sheet_name='importar')


def de_para_servicos(de):
    de = de.strip()
    para = '***idefinido***'
    if de in ('Bebedouros - ADM',):
        para = 'Bebedouro'
    if de in ('Cenotecnia Teatro - CEUs.',):
        para = 'Cenotécnica Teatro'
    if de in ('Controle de Pragas e Insetos - CEUs.',):
        para = 'Controle de Pragas e Insetos'
    if de in ('Copeiragem - ADM',):
        para = 'Copeiragem'
    if de in ('Correios - ADM - Postagem',):
        para = 'Correios'
    if de in ('Iluminação Teatros - CEUs. - Emergencial',):
        para = 'Iluminação de teatros'
    if de in ('Lavanderia - CEIs. em CEUs.',):
        para = 'Lavanderia do Centro de Educação Infantil'
    if de in (
        'Limpeza - ADM - Emergencial',
        'Limpeza - CECIs.',
        'Limpeza - CEUs.',
        'Limpeza - UEs.',
        'Limpeza - UEs. - EMEF/EMEFM/CIEJA/CMCT/EMEB/INST. FEDERAL - Emergencial 01',
        'Limpeza - UEs. - Emergencial',
        'Limpeza - UEs. - EMEF/EMEFM/CIEJA/CMCT/EMEB/INST. FEDERAL - Emergencial 02',
    ):
        para = 'Limpeza'

    if de in ("Limpeza de Caixa D'Agua - CEUs.",):
        para = "Limpeza de Caixa d'água"
    if de in ('Manutenção Cabines Primárias',):
        para = 'Manutenção de cabines primárias '
    if de in ('Manutenção de Elevadores',):
        para = 'Manutenção de elevadores'
    if de in ('Manutenção Eletrica Piscina - CEUs.',):
        para = 'Manutenção Elétrica de Piscinas'
    if de in ('Monitoramento Aquático - CEUs.',):
        para = 'Monitoramento Aquático'
    if de in ('Limpeza de Piscina - CEUs. - Emergencial',):
        para = 'Operador de Piscina'
    if de in ('PABX - ADM',):
        para = 'PABX'
    if de in ('Recepção e Portaria - ADM',):
        para = 'Recepção e Portaria'
    if de in ('Sistema de Telefonia Fixa Comodata - Operação STF',):
        para = 'Sistema de telefonia fixa Comodata'
    if de in ('Som Teatros - CEUs. - Emergencial',):
        para = 'Som teatros'
    if de in ('Telefonia Movel  - ADM',):
        para = 'Telefonia Móvel'
    if de in ('Telefonista - SME',):
        para = 'Telefonista'
    if de in (
        'Vigilância - ADM',
        'Vigilancia - CECIs. - Emergencial',
        'Vigilancia - CEUs.',
        'Vigilancia - UEs.',
        'Vigilancia - UEs. - Emergencial'
    ):
        para = 'Telefonista'

    return para


def importa_empresa(empresa_data: dict):
    if not Empresa.objects.filter(cnpj=empresa_data['cnpj']).exists():
        print(f"Criada empresa {empresa_data['nome']} CNPJ:{empresa_data['cnpj']}")
        Empresa.objects.create(**empresa_data)


def importa_contratos():
    for index, row in df.iterrows():
        empresa_data = {
            'nome': row['EMPRESA'],
            'cnpj': clean_id(row['CNPJ'])
        }
        importa_empresa(empresa_data)
        tc = row['TC']
        servico = de_para_servicos(row["OBJETO"])
        cnpj = clean_id(row['CNPJ'])
        inicio = row['INICIO']
        print(f'Cont:{index} TC:{tc} - CNPJ:{empresa_data["cnpj"]}-{empresa_data["nome"]}')

    if __name__ == '__main__':
        importa_contratos()
