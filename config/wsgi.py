import os
import sys

# Добавьте путь к вашему проекту
path = '/home/kuromi/1_sem_hacaton_mast_syr'
if path not in sys.path:
    sys.path.append(path)

# Укажите путь к settings.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()