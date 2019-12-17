import logging

import environ
from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

env = environ.Env()


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


def enviar_email_html(assunto, template, data, enviar_para):
    try:
        config = DynamicEmailConfiguration.get_solo()

        msg_html = render_to_string(f"email/{template}.html", data)

        msg = EmailMessage(
            subject=assunto, body=msg_html,
            from_email=config.from_email or None,
            bcc=(enviar_para,),
        )
        msg.content_subtype = "html"  # Main content is now text/html

        msg.send()

    except Exception as err:
        logger.error(str(err))
