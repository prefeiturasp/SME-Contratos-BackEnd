from .models import ParametroNotificacoesVigencia, Contrato, NotificacaoVigenciaContrato


def gera_notificacoes_vigencia_contratos():
    for estado in Contrato.ESTADOS:
        parametros = ParametroNotificacoesVigencia.parametros_do_estado(estado)
        if not parametros:
            continue

        data_limite = ParametroNotificacoesVigencia.data_limite_do_estado(estado)

        contratos = Contrato.contratos_no_estado(estado).filter(data_encerramento__lte=data_limite).all()

        for contrato in contratos:
            try:
                notificacao_gestor = NotificacaoVigenciaContrato.objects.get(contrato=contrato,
                                                                             notificado=contrato.gestor)

            except NotificacaoVigenciaContrato.DoesNotExist:
                notificacao_gestor = None

    # Busca parâmetros para a memória
    # Por Estado
    #   Dias pra Vencer   Repedir a cada
    #   100               30
    #    50               15
    #    10                1

    # Para cada estado
    #   Pegar maior (Dias pra vencer) dos parâmetros
    #   Filtrar os contratos do estado e prazo_pra_vencer < maior_dias_a_vencer_do_parametro
    #   Para cada contrato
    #       Se não tem notificação:
    #           Gravar Notificação
    #       Se tem notificação
    #           Pegar tempo de repetição do dias_pra_vencer do contrato
    #           Se a ultima notificação foi a mais dias que o tempo de repetição
    #               Atualizar notificação
    #               Enviar nova notificação
