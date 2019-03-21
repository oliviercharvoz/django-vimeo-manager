# -*- coding: utf-8 -*-

from django.contrib import admin

from ..models.album import Album
from .collection import CollectionAdmin


@admin.register(Album)
class AlbumAdmin(CollectionAdmin):
    pass
