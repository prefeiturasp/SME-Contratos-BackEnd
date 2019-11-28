import logging

from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def enviar_email(assunto, mensagem, enviar_para):
    try:
        config = DynamicEmailConfiguration.get_solo()
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=config.from_email or None,
            recipient_list=[enviar_para]
        )
    except Exception as err:
        logger.error(str(err))


def enviar_email_html(assunto, mensagem, enviar_para):
    try:
        config = DynamicEmailConfiguration.get_solo()
        send_mail(
            subject=assunto,
            html_mensage=mensagem,
            from_email=config.from_email or None,
            recipient_list=[enviar_para]
        )
    except Exception as err:
        logger.error(str(err))

