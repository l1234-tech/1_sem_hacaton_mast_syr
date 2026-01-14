from django.apps import AppConfig

class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'

    def ready(self):
        """Инициализация приложения"""
        try:
            import notes.signals
            import notes.context_processors
        except ImportError:
            pass