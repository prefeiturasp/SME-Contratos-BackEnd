from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "sme_coad_apps.users"
    verbose_name = 'Usuário'
    verbose_name_plural = 'Usuários'

    def ready(self):
        try:
            import sme_coad_apps.users.signals  # noqa F401
        except ImportError:
            pass
