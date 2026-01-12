import os
import sys

# Путь к вашему проекту на PythonAnywhere
path = '/home/ваше_имя_на_pythonanywhere/ваша_папка_проекта'
if path not in sys.path:
    sys.path.append(path)

# Указываем Django, какой файл настроек использовать
os.environ['DJANGO_SETTINGS_MODULE'] = 'notes_project.settings'

# Импортируем WSGI приложение Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()