# -*- coding: utf-8 -*-

from django.utils.translation import pgettext_lazy

from .collection import Collection


class Album(Collection):
    endpoint = '/me/albums'

    class Meta:
        verbose_name = pgettext_lazy('Album model', 'album')
        verbose_name_plural = pgettext_lazy('Album model', 'albums')
