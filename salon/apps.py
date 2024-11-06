from django.apps import AppConfig


class SalonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salon'
    
    def ready(self) -> None:
        import salon.signals
