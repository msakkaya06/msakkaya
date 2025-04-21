# easymanagement/apps.py
from django.apps import AppConfig

class EasymanagementConfig(AppConfig):
    name = 'easymanagement'

    def ready(self):
        import EasyEating.signals
