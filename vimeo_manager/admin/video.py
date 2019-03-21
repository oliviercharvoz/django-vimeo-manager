# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.utils.translation import pgettext_lazy

from ..models.video import Video
from ..utils import send_video_approval_request_email
from .resource import ResourceAdmin


@admin.register(Video)
class VideoAdmin(ResourceAdmin):
    actions = ResourceAdmin.actions + (
        'request_approval_action',
    )
    fields = ResourceAdmin.fields + (
        ('created_datetime', 'modified_datetime'), 'video_embed', 'approval_status', 'name', 'description', 'tags',
    )
    readonly_fields = ResourceAdmin.readonly_fields + (
        'video_embed', 'created_datetime', 'modified_datetime',
    )
    list_display = ResourceAdmin.list_display + (
        'thumbnail', 'name', 'link', 'created_datetime', 'modified_datetime', 'approval_status', 'synchronized',
    )
    list_display_links = ('thumbnail', 'name')
    list_filter = ResourceAdmin.list_filter + (
        'approval_status',
    )
    search_fields = ('^name', '^tags', '^description')

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Validation').count():
            return VideoAdmin.readonly_fields
        return VideoAdmin.readonly_fields + ('approval_status', )

    def link(self, obj):
        return obj.html_link

    link.allow_tags = True
    link.short_description = pgettext_lazy('Video admin', 'link')

    def thumbnail(self, obj):
        return obj.html_thumbnail

    thumbnail.allow_tags = True
    thumbnail.short_description = pgettext_lazy('Video admin', 'thumbnail')

    def video_embed(self, obj):
        return obj.html_video_embed

    video_embed.allow_tags = True
    video_embed.short_description = pgettext_lazy('Video admin', 'video embed')

    def request_approval_action(self, request, queryset):
        """ Request approval action """
        sent = send_video_approval_request_email(request, queryset)

        if sent:
            messages.success(request, pgettext_lazy('Video approval request email',
                                                    'Your video approval request has been sent'))
            queryset.update(approval_status=Video.APPROVAL_STATUS_PENDING_APPROVAL)
        else:
            messages.error(request, pgettext_lazy('Video approval request email',
                                                  'Your video approval request could not be sent'))

    request_approval_action.short_description = pgettext_lazy('Video admin', 'Request approval')
