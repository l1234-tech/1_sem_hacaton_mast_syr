from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'

    def ready(self):
        """Инициализация приложения"""
        # Импортируем контекстные процессоры и сигналы
        try:
            import notes.signals  # если будут сигналы
            import notes.context_processors
        except ImportError:
            pass