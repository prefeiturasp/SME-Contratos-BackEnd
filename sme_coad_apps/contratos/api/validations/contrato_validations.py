from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from sme_coad_apps.contratos.models import Ata, Empresa, Produto

# ####### Constantes de Produto #######
# Categorias
OUTROS = Produto.CATEGORIA_OUTROS
ALIMENTO = Produto.CATEGORIA_ALIMENTO
# Gupos Alimentares
CONGELADOS = Produto.GRUPO_ALIMENTAR_CONGELADOS
FLVO = Produto.GRUPO_ALIMENTAR_FLVO
PAES_E_BOLO = Produto.GRUPO_ALIMENTAR_PAES_E_BOLO
SECOS = Produto.GRUPO_ALIMENTAR_SECOS
# Armazenabilidades
ARMAZENAVEL = Produto.ARMAZENABILIDADE_ARMAZENAVEL
NAO_ARMAZENAVEL = Produto.ARMAZENABILIDADE_NAO_ARMAZENAVEL
# Durabilidades
PERECIVEL = Produto.DURABILIDADE_PERECIVEL
NAO_PERECIVEL = Produto.DURABILIDADE_NAO_PERECIVEL


def nao_pode_repetir_o_gestor(gestores):
    lista_gestores = []
    if gestores:
        for gestor in gestores:
            for _key, value in gestor.items():
                lista_gestores.append(value)
        if len(lista_gestores) != len(set(lista_gestores)):
            raise serializers.ValidationError({'detail': 'Não é permitido duplicidade de gestor no contrato'})


def data_encerramento(unidade_vigencia, vigencia, data_assinatura, data_encerramento):
    data_referencia = datetime.strptime(data_assinatura, '%Y-%m-%d').date()
    data_encerramento_payload = datetime.strptime(data_encerramento, '%Y-%m-%d').date()
    if unidade_vigencia == Ata.UNIDADE_VIGENCIA_MESES:
        data_calculada = data_referencia + relativedelta(months=+vigencia) - relativedelta(days=+1)
    else:
        data_calculada = data_referencia + relativedelta(days=+vigencia)

    if data_encerramento_payload != data_calculada:
        raise serializers.ValidationError({'detail': 'Data de encerramento não está correta'})


def tipo_fornecimento(tipo_servico):
    if tipo_servico == Empresa.ARMAZEM_DISTRIBUIDOR:
        raise serializers.ValidationError({'detail': f'Não é possivel informar Tipo de fornecedor caso o tipo de '
                                                     f'serviço seja {Empresa.ARMAZEM_DISTRIBUIDOR}.'})


def produto_validation(categoria, grupo_alimentar, durabilidade, armazenabilidade):
    msg = 'Durabilidade ou armazenabilidade invalida para o grupo alimentar escolhido.'
    if categoria == OUTROS:
        if durabilidade or grupo_alimentar:
            raise serializers.ValidationError({
                'detail': f'Não é permitido informar durabilidade ou grupo alimentar quando a categoria é {OUTROS}'})
    if categoria == ALIMENTO:
        if grupo_alimentar == SECOS:
            if durabilidade != NAO_PERECIVEL or armazenabilidade != ARMAZENAVEL:
                raise serializers.ValidationError({'detail': msg})

        if grupo_alimentar == CONGELADOS:
            if durabilidade != PERECIVEL or armazenabilidade != ARMAZENAVEL:
                raise serializers.ValidationError({'detail': msg})

        if grupo_alimentar == FLVO or grupo_alimentar == PAES_E_BOLO:
            if durabilidade != PERECIVEL or armazenabilidade != NAO_ARMAZENAVEL:
                raise serializers.ValidationError({'detail': msg})
