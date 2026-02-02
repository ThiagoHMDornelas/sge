from django.apps import AppConfig


class InflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inflow'

    def ready(self):
        import inflow.signals  # noqa: F401
