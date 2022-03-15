from smtplib import SMTPServerDisconnected

import environ
from celery import shared_task

from sme_coad_apps.core.helpers.enviar_email import enviar_email_html

env = environ.Env()


# https://docs.celeryproject.org/en/latest/userguide/tasks.html
@shared_task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def enviar_email_redefinicao_senha(email, username, nome, hash_redefinicao):
    link = f'http://{env("SERVER_NAME")}/#/login/?hash={hash_redefinicao}'
    return enviar_email_html(
        'Solicitação de redefinição de senha',
        'email_redefinicao_de_senha',
        {'url': link,
         'nome': nome,
         'login': username,
         },
        email
    )
