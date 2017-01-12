from __future__ import unicode_literals

from django.apps import AppConfig


class InicioConfig(AppConfig):
    name = 'inicio'

    def ready(self):
        import inicio.signals
