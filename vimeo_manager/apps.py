from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VimeoManagerConfig(AppConfig):
    name = 'vimeo_manager'
    verbose_name = _('Vimeo manager')
