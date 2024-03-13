from django.apps import AppConfig


class FilerobotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filerobot'

    def ready(self):
        from . import signals

