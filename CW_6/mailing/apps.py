from django.apps import AppConfig
from django.conf import settings

class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'
    verbose_name = 'рассылки'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from CW_6 import operator
            operator.start()

