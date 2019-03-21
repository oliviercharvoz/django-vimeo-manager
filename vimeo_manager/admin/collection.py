# -*- coding: utf-8 -*-

from django.utils.translation import pgettext_lazy

from .resource import ResourceAdmin


class CollectionAdmin(ResourceAdmin):
    fields = ResourceAdmin.fields + (
        ('created_datetime', 'modified_datetime'), 'link', 'name', 'description', 'videos',
    )
    readonly_fields = ResourceAdmin.readonly_fields + (
        'link', 'created_datetime', 'modified_datetime',
    )
    list_display = ResourceAdmin.list_display + (
        'thumbnail', 'name', 'link', 'created_datetime', 'modified_datetime', 'synchronized',
    )
    list_display_links = ('thumbnail', 'name')
    search_fields = ('^name', '^description')

    def link(self, obj):
        """ HTML link to collection """
        return '<a target="_blank" href="%(url)s">%(url)s</a>' % {
            'url': obj.url,
        }

    link.allow_tags = True
    link.short_description = pgettext_lazy('Collection admin', 'link')

    def thumbnail(self, obj):
        return obj.html_thumbnail

    thumbnail.allow_tags = True
    thumbnail.short_description = pgettext_lazy('Collection admin', 'thumbnail')

    def update_from_vimeo_action(self, request, queryset):
        """ Update from vimeo action """
        self.model.objects.update_from_vimeo()

    update_from_vimeo_action.short_description = pgettext_lazy('Resource admin', 'Update from Vimeo')
