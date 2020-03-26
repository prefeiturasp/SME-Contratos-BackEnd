import logging

from config import celery_app
from .models.notificacao_vigencia_contrato import NotificacaoVigenciaContrato

logger = logging.getLogger('safi.tasks_contratos')


@celery_app.task()
def gera_notificacoes_vigencia_contrato():
    logger.info('Iniciando notificações de vigência...')
    NotificacaoVigenciaContrato.gera_notificacoes()
    logger.info('Fim notificações de vigência...')
