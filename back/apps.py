from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'back'

    def ready(self):
        from back.signals import group_init
        post_migrate.connect(group_init, sender=self)
