import logging

from django.utils import timezone

from config import celery_app
from .models.notificacao_vigencia_contrato import NotificacaoVigenciaContrato
from .models.contrato import Contrato

logger = logging.getLogger('safi.tasks_contratos')


@celery_app.task()
def gera_notificacoes_vigencia_contrato():
    logger.info('Iniciando notificações de vigência...')
    NotificacaoVigenciaContrato.gera_notificacoes()
    logger.info('Fim notificações de vigência...')


@celery_app.task()
def encerra_contratos_vencidos():
    logger.info('Iniciando encerramento de contratos vencidos...')
    contratos = Contrato.objects.filter(data_encerramento__lt=timezone.now()).exclude(
        situacao=Contrato.SITUACAO_ENCERRADO)

    for contrato in contratos:
        logger.info(f'Encerrando Contrato: {contrato.termo_contrato}')
        contrato.situacao = Contrato.SITUACAO_ENCERRADO
        contrato.save()

    logger.info('Fim encerramento de contratos vencidos...')
