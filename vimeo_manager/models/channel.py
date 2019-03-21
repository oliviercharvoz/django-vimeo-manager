# -*- coding: utf-8 -*-

from django.utils.translation import pgettext_lazy

from .collection import Collection


class Channel(Collection):
    endpoint = '/me/channels'

    class Meta:
        verbose_name = pgettext_lazy('Channel model', 'channel')
        verbose_name_plural = pgettext_lazy('Channel model', 'channels')
