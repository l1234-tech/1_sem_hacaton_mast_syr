"""
Контекстные процессоры для приложения notes.
Добавляют дополнительные переменные во все шаблоны.
"""

from django import get_version

def django_version(request):
    """Добавляет версию Django в контекст шаблонов"""
    return {
        'django_version': get_version(),
    }