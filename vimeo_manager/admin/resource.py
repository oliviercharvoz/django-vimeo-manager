# -*- coding: utf-8 -*-

from django.contrib import admin, messages
from django.utils.translation import pgettext_lazy


class ResourceAdmin(admin.ModelAdmin):
    actions = ('update_from_vimeo_action', )
    fields = ('synchronized', )
    readonly_fields = ('synchronized', )
    list_display = ()
    list_filter = ('synchronized', )
    ordering = ('-modified_datetime', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ResourceAdmin, self).get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        super(ResourceAdmin, self).save_model(request, obj, form, change)
        obj.save()
        synchronized = obj.export_to_vimeo()

        if synchronized:
            messages.success(request, pgettext_lazy('Resource synchronization',
                                                    '%(resource_class_name)s object "%(resource_name)s" '
                                                    'has been successfully synchronized.') % {
                                                        'resource_class_name': obj.__class__.__name__,
                                                        'resource_name': obj.name,
                                                    })
        else:
            messages.error(request, pgettext_lazy('Resource synchronization',
                                                  'The synchronization of the %(resource_class_name)s object '
                                                  '"%(resource_name)s" has failed.') % {
                                                        'resource_class_name': obj.__class__.__name__,
                                                        'resource_name': obj.name,
                                                    })

    def update_from_vimeo_action(self, request, queryset):
        """ Update from Vimeo action """
        self.model.objects.update_and_import_videos_from_vimeo()
