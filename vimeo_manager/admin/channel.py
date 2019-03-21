# -*- coding: utf-8 -*-

from django.contrib import admin

from ..models.channel import Channel
from .collection import CollectionAdmin


@admin.register(Channel)
class ChannelAdmin(CollectionAdmin):
    pass
