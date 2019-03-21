# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import pgettext_lazy

from ..utils import VimeoManager, VimeoException
from ..managers.resource import ResourceManager


class Resource(models.Model):
    synchronized = models.BooleanField(
        verbose_name=pgettext_lazy('Resource field', 'synchronized'),
        default=True
    )
    last_import_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Resource field', 'last import'),
        null=True, blank=True
    )
    last_export_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Resource field', 'last export'),
        null=True, blank=True
    )

    # Vimeo properties
    uri = models.CharField(
        verbose_name=pgettext_lazy('Resource field', 'uri'),
        max_length=50
    )

    objects = ResourceManager()

    class Meta:
        abstract = True

    @property
    def endpoint(self):
        raise NotImplementedError

    @property
    def vimeo_id(self):
        return self.uri.split('/')[-1]

    @classmethod
    def import_all_from_vimeo(cls):
        """
        Creates, updates or deletes Resource instances
        with the data from the Vimeo objects returned by the Resource endpoint
        """
        v_objs = VimeoManager.get_objects_from_vimeo(cls.endpoint)
        objs = cls.objects.all()
        objs_to_delete = set([x.uri for x in objs]).difference([x['uri'] for x in v_objs])

        for obj_uri in objs_to_delete:
            cls.objects.get(uri=obj_uri).delete()

        for v_obj in v_objs:
            cls.import_from_vimeo_object(v_obj)

    @classmethod
    def import_from_vimeo_object(cls, v_obj):
        """
        Creates or updates one Resource instance with the data from a Vimeo object

        :param v_obj: the Vimeo object
        :return: a tuple (obj, created), where created is a boolean specifying whether an object was created
            and obj is the object
        """
        raise NotImplementedError

    def update_from_vimeo(self):
        """
        Updates the Resource instance with the data from Vimeo

        :return: a boolean specifying if the instance has been updated or not
        """
        try:
            v_obj = VimeoManager.get_objects_from_vimeo(self.uri)
            self.import_from_vimeo_object(v_obj)
        except VimeoException:
            return False
        return True

    def export_to_vimeo(self):
        """
        Exports Resource to Vimeo

        :return: a boolean specifying if the Resource has been exported or not
        """
        raise NotImplementedError
