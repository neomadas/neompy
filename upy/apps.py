from django.apps import AppConfig
from django.conf import settings


class UpyConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'upy'

  def ready(self):
    from upy.core.ioc import manager
    settings.UPY_IOC_WIRES(manager)
