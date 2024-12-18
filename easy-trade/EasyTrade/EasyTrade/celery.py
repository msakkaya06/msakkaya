# your_project/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.conf import settings

# Django'nun settings modülünü çevre değişkeni olarak belirleyin.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyTrade.settings')

app = Celery('EasyTrade')

# Celery konfigürasyonlarını ayarlayın
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.imports = ('EasyTrade.tasks',)
# Django'nun uygulama modüllerinden görevler yükleyin
app.autodiscover_tasks()
