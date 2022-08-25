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


def campo_nao_pode_ser_nulo(valor, mensagem='Não pode ser nulo'):
    if not valor:
        raise serializers.ValidationError(mensagem)


def validacao_objetos_aditamento(attrs):
    objetos_aditamento = attrs['objeto_aditamento']
    objetos = ['PRORROGACAO_VIGENCIA_CONTRATUAL', 'MODIFICACAO_PROJETO_ESPECIFICACOES', 'MODIFICACAO_VALOR_CONTRATUAL']
    for objeto in objetos:
        if objeto in objetos_aditamento:
            campo_nao_pode_ser_nulo(attrs.get('valor_mensal_atualizado', None),
                                    mensagem='Valor mensal atualizado obrigatório.')
            campo_nao_pode_ser_nulo(attrs.get('valor_total_atualizado', None),
                                    mensagem='Valor total atualizado obrigatório')
            campo_nao_pode_ser_nulo(attrs.get('data_inicial', None),
                                    mensagem='Data inicial obrigatória')
            campo_nao_pode_ser_nulo(attrs.get('data_final', None),
                                    mensagem='Data final obrigatória')
            if 'MODIFICACAO_VALOR_CONTRATUAL' in objetos_aditamento:
                campo_nao_pode_ser_nulo(attrs.get('valor_aditamento', None),
                                        mensagem='Valor do aditamento obrigatório.')


def validacao_data_rescisao(attrs):
    contrato = attrs['contrato']
    data_rescicao = attrs['data_rescisao']
    data_inicio = (contrato.data_assinatura if contrato.referencia_encerramento == 'DATA_ASSINATURA'
                   else contrato.data_ordem_inicio)
    data_encerramento = contrato.data_encerramento

    if data_rescicao < data_inicio:
        raise serializers.ValidationError('Data de rescisão anteior a data de início do contrato')
    elif data_rescicao > data_encerramento:
        raise serializers.ValidationError('Data de rescisão superior a data de vencimento do contrato')
