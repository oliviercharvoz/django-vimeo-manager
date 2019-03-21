# -*- coding: utf-8 -*-

from django.db.models import manager


class ResourceManager(manager.Manager):
    def update_from_vimeo(self):
        """
        Updates the Resources in the queryset with the data from Vimeo

        :return: a boolean specifying if the instances have been updated or not
        """
        updated = True

        for resource in self.get_queryset():
            updated = resource.update_from_vimeo()

        return updated
