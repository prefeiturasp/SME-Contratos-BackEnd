from notifications.signals import notify

from .models import ParametroNotificacoesVigencia, Contrato, NotificacaoVigenciaContrato


def gera_notificacoes_vigencia_contratos():
    for estado in Contrato.ESTADOS:

        if not ParametroNotificacoesVigencia.estado_notificavel(estado):
            continue

        data_limite = ParametroNotificacoesVigencia.data_limite_do_estado(estado)

        contratos = Contrato.contratos_no_estado(estado, vencendo_ate=data_limite)

        for contrato in contratos:
            if not contrato.gestor:
                continue

            frequencia_de_notificacao = ParametroNotificacoesVigencia.frequencia_repeticao(
                estado, dias_pra_vencer=contrato.dias_para_o_encerramento
            )

            ultima_notificacao = NotificacaoVigenciaContrato.ultima_notificacao_para_o_gestor_do_contrato(contrato)

            if not ultima_notificacao or ultima_notificacao.idade >= frequencia_de_notificacao:
                notificacao = NotificacaoVigenciaContrato.objects.create(
                    contrato=contrato,
                    notificado=contrato.gestor,
                )

                notify.send(
                    notificacao,
                    verb='alerta_vigencia_contrato',
                    recipient=notificacao.notificado,
                    description=f'O contrato {contrato.termo_contrato} '
                                f'está a {contrato.dias_para_o_encerramento} de seu encerramento.',
                    target=contrato,
                )
