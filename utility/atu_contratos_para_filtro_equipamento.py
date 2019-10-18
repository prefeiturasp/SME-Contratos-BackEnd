"""
Esse programa atualiza os contratos para responderem corretamente ao filtro por equipamento.


Para rodar esse programa:

    - Executar o shell_plus
    - Importar desse arquivo a função atualiza_filtro_equipamento_nos_contratos
    - Executar a função atualiza_filtro_equipamento_nos_contratos()

"""

from sme_coad_apps.contratos.models import Contrato


def atualiza_filtro_equipamento_nos_contratos():
    for contrato in Contrato.objects.all():
        contrato.save()


