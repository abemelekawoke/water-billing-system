from django.apps import AppConfig

class ReadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reads'

    # def ready(self):
    #     import reads.signals  # Ensure signals are loaded when the app starts
