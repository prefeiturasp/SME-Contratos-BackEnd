from datetime import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from sme_coad_apps.contratos.models import Ata, Empresa


def gestor_e_suplente_devem_ser_diferentes(gestor, suplente):
    if gestor and gestor == suplente:
        raise serializers.ValidationError({'detail': 'Gestor e Suplente devem ser diferentes'})


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
