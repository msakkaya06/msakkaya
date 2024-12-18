# myproject/__init__.py

from __future__ import absolute_import, unicode_literals

# Bu dosya Celery uygulamanızı başlatır
from .celery import app as celery_app

__all__ = ('celery_app',)
