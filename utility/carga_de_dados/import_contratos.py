import environ
import pandas as pd
from auditlog.registry import auditlog
from brazilnum.cnpj import clean_id
from django.db.models import F

from sme_coad_apps.contratos.models import Empresa, Objeto, Contrato, ContratoUnidade, FiscaisUnidade
from sme_coad_apps.contratos.models.contrato import AnexoContrato
from sme_coad_apps.core.models import Divisao, Nucleo, Unidade, Coad
from utility.carga_de_dados.import_dres import importa_dres

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


def cria_digecon():
    digecon = Divisao.objects.filter(sigla='DIGECON')
    if digecon.exists():
        return digecon.first()
    else:
        print(f"Criada divisão DIGECON.")
        return Divisao.objects.create(sigla='DIGECON', nome='Divisão de Gestão de Contratos')


def cria_nucleos(divisao):
    nuad = cria_nucleo(divisao, sigla='NUAD', nome='Núcleo de Unidades Administrativas')
    nuceu = cria_nucleo(divisao, sigla='NUCEU', nome='Núcleo de Centros Educacionais Unificados')
    nue = cria_nucleo(divisao, sigla='NUE', nome='Núcleo de Unidades Escolares')
    return {
        Unidade.EQP_UNIDADE_ADMINISTRATIVA: nuad,
        Unidade.EQP_UNIDADE_CEU: nuceu,
        Unidade.EQP_UNIDADE_ENSINO: nue
    }


def cria_nucleo(divisao, sigla, nome):
    busca_sigla = Nucleo.objects.filter(sigla=sigla)
    if busca_sigla.exists():
        return busca_sigla.first()
    else:
        print(f'Criado Núcleo {sigla}')
        return Nucleo.objects.create(sigla=sigla, nome=nome, divisao=divisao)


def de_para_servicos(de):
    de = de.strip()

    if de in ('Bebedouros - ADM',):
        para = 'Bebedouro'
    elif de in ('Cenotecnia Teatro - CEUs.',):
        para = 'Cenotécnica Teatro'
    elif de in ('Controle de Pragas e Insetos - CEUs.',):
        para = 'Controle de Pragas e Insetos'
    elif de in ('Copeiragem - ADM',):
        para = 'Copeiragem'
    elif de in ('Correios - ADM - Postagem',):
        para = 'Correios'
    elif de in ('Iluminação Teatros - CEUs. - Emergencial',):
        para = 'Iluminação de teatros'
    elif de in ('Lavanderia - CEIs. em CEUs.',):
        para = 'Lavanderia do Centro de Educação Infantil'
    elif de in (
        'Limpeza - ADM - Emergencial',
        'Limpeza - CECIs.',
        'Limpeza - CEUs.',
        'Limpeza - UEs.',
        'Limpeza - UEs. - EMEF/EMEFM/CIEJA/CMCT/EMEB/INST. FEDERAL - Emergencial 01',
        'Limpeza - UEs. - Emergencial',
        'Limpeza - UEs. - EMEF/EMEFM/CIEJA/CMCT/EMEB/INST. FEDERAL - Emergencial 02',
    ):
        para = 'Limpeza'

    elif de in ("Limpeza de Caixa D'Agua - CEUs.",):
        para = "Limpeza de Caixa d'água"
    elif de in ('Manutenção Cabines Primárias',):
        para = 'Manutenção de cabines primárias '
    elif de in ('Manutenção de Elevadores',):
        para = 'Manutenção de elevadores'
    elif de in ('Manutenção Eletrica Piscina - CEUs.',):
        para = 'Manutenção Elétrica de Piscinas'
    elif de in ('Monitoramento Aquático - CEUs.',):
        para = 'Monitoramento Aquático'
    elif de in ('Limpeza de Piscina - CEUs. - Emergencial',):
        para = 'Operador de Piscina'
    elif de in ('PABX - ADM',):
        para = 'PABX'
    elif de in ('Recepção e Portaria - ADM',):
        para = 'Recepção e Portaria'
    elif de in ('Sistema de Telefonia Fixa Comodata - Operação STF',):
        para = 'Sistema de telefonia fixa Comodata'
    elif de in ('Som Teatros - CEUs. - Emergencial',):
        para = 'Som teatros'
    elif de in ('Telefonia Movel  - ADM',):
        para = 'Telefonia Móvel'
    elif de in ('Telefonista - SME',):
        para = 'Telefonista'
    elif de in (
        'Vigilância - ADM',
        'Vigilancia - CECIs. - Emergencial',
        'Vigilancia - CEUs.',
        'Vigilancia - UEs.',
        'Vigilancia - UEs. - Emergencial'
    ):
        para = 'Telefonista'
    else:
        para = '***idefinido***'

    return para


def de_para_equipamento(de):
    de = de.strip()

    if de in ('ADM', 'DRE', 'IFSP', 'CMCT'):
        para = Unidade.EQP_UNIDADE_ADMINISTRATIVA
    elif de in ('CECI', 'CEI', 'CEMEI', 'CIEJA', 'EMEBS', 'EMEF', 'EMEFM', 'EMEI'):
        para = Unidade.EQP_UNIDADE_ENSINO
    elif de in ('CEU',):
        para = Unidade.EQP_UNIDADE_CEU
    else:
        para = '***idefinido***'

    return para


def de_para_estado(de):
    de = de.strip()

    if de == 'ÚLTIMO ANO':
        para = 'ULTIMO_ANO'
    elif de == 'EXCEPCIONALIDADE':
        para = 'EXCEPCIONAL'
    else:
        para = de
    return para


def importa_empresa(empresa_data: dict):
    empresa = Empresa.objects.filter(cnpj=empresa_data['cnpj'])
    if not empresa.exists():
        print(f"Criada empresa {empresa_data['nome']} CNPJ:{empresa_data['cnpj']}")
        return Empresa.objects.create(**empresa_data)
    else:
        return empresa.first()


def importa_objeto(objeto_data: dict):
    objeto = Objeto.objects.filter(nome=objeto_data['nome'])
    if not objeto.exists():
        print(f"Criado tipo de serviço {objeto_data['nome']}")
        return Objeto.objects.create(**objeto_data)
    else:
        return objeto.first()


def importa_unidade(unidade_data: dict):
    unidade = Unidade.objects.filter(codigo_eol=unidade_data['codigo_eol'])
    if not unidade.exists():
        print(f"Criada Unidade {unidade_data['nome']}")
        return Unidade.objects.create(**unidade_data)
    else:
        return unidade.first()


def apaga_contratos():
    Contrato.objects.all().delete()
    print('Contratos apagados.')


def importa_contrato(contrato_data: dict):
    contrato = Contrato.objects.filter(termo_contrato=contrato_data['termo_contrato'])
    if not contrato.exists():
        print(f"Criado Contrato {contrato_data['termo_contrato']}")
        novo_contrato = Contrato(**contrato_data)
        novo_contrato.save()
        return novo_contrato
    else:
        return contrato.first()


def importa_contrato_detalhe(contrato_detalhe_data: dict):
    contrato_detalhe = ContratoUnidade.objects.filter(contrato=contrato_detalhe_data['contrato'],
                                                      unidade=contrato_detalhe_data['unidade'])

    if not contrato_detalhe.exists():
        print(
            f"Criado Contrato Detalhe TC:{contrato_detalhe_data['contrato'].termo_contrato} "
            f"EOL:{contrato_detalhe_data['unidade'].codigo_eol}")
        ContratoUnidade.objects.create(**contrato_detalhe_data)
    else:
        print(
            f"Atualizado Contrato Detalhe TC:{contrato_detalhe_data['contrato'].termo_contrato} "
            f"EOL:{contrato_detalhe_data['unidade'].codigo_eol}")
        contrato_detalhe.update(valor_mensal=F('valor_mensal') + contrato_detalhe_data['valor_mensal'])


def grava_dotacoes(dotacoes):
    for termo_contrato in dotacoes:
        Contrato.objects.filter(termo_contrato=termo_contrato).update(
            dotacao_orcamentaria=list(dotacoes[termo_contrato]))
        print(f'Gravadas dotações do TC: {termo_contrato}', dotacoes[termo_contrato])


def cria_coad():
    if not Coad.objects.exists():
        return Coad.objects.create()
    else:
        return Coad.objects.first()


def importa_contratos():
    auditlog.unregister(Contrato)
    auditlog.unregister(ContratoUnidade)
    auditlog.unregister(AnexoContrato)
    auditlog.unregister(FiscaisUnidade)
    auditlog.unregister(Divisao)
    auditlog.unregister(Nucleo)
    auditlog.unregister(Unidade)
    auditlog.unregister(Coad)

    cria_coad()

    digecon = cria_digecon()
    nucleos = cria_nucleos(digecon)

    dotacoes = {}

    apaga_contratos()

    for index, row in df.iterrows():
        tc = row['TC'].strip()
        eol_unidade = row['EOL_UNIDADE'].strip()

        print(f'Cont:{index} Importando Linha:{row["LINHA"]} TC:{tc}')

        empresa_data = {
            'nome': row['EMPRESA'],
            'cnpj': clean_id(row['CNPJ'])
        }
        empresa_contratada = importa_empresa(empresa_data)

        servico = de_para_servicos(row["OBJETO"])
        objeto = importa_objeto({'nome': servico})

        equipamento = de_para_equipamento(row['EQP'])

        delta = row['TERMINO'] - row['INICIO']
        vigencia = delta.days
        unidade_vigencia = Contrato.UNIDADE_VIGENCIA_DIAS

        unidade_data = {
            'codigo_eol': eol_unidade,
            'nome': row['NOME_UNIDADE'],
            'equipamento': equipamento,
            'tipo_unidade': row['EQP']
        }
        unidade = importa_unidade(unidade_data)

        contrato_data = {
            'termo_contrato': tc,
            'processo': row['PROCESSO'],
            'objeto': objeto,
            'nucleo_responsavel': nucleos[equipamento],
            'empresa_contratada': empresa_contratada,
            'data_ordem_inicio': row['INICIO'],
            'unidade_vigencia': unidade_vigencia,
            'vigencia': vigencia,
            'situacao': Contrato.SITUACAO_ATIVO,
            'data_encerramento': row['TERMINO']
        }

        contrato = importa_contrato(contrato_data)

        contrato_detalhe_data = {
            'contrato': contrato,
            'unidade': unidade,
            'valor_mensal': row['TOTAL_MENSAL'],
            # TODO Rever a gravação de dotações em função de mudanças do modelo após importação inicial.
            # 'dotacao_orcamentaria': row['DOTACAO'],
            'lote': row['LOTE'],
        }

        importa_contrato_detalhe(contrato_detalhe_data)

        # Grava dotacoes do contrato
        if contrato.termo_contrato not in dotacoes:
            dotacoes[contrato.termo_contrato] = set()

        dotacoes[contrato.termo_contrato].add(row['DOTACAO'])

    # importa_dres()

    # grava_dotacoes(dotacoes)

    if __name__ == '__main__':
        importa_contratos()
