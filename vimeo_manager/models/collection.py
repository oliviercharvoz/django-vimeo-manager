# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import pgettext_lazy

from ..utils import VimeoManager, VimeoException
from ..managers.collection import CollectionManager
from .resource import Resource
from .video import Video


@python_2_unicode_compatible
class Collection(Resource):
    # Vimeo properties
    name = models.CharField(
        verbose_name=pgettext_lazy('Collection field', 'name'),
        max_length=100
    )
    description = models.TextField(
        verbose_name=pgettext_lazy('Collection field', 'description'),
        null=True, blank=True
    )
    url = models.URLField(
        verbose_name=pgettext_lazy('Collection field', 'url')
    )
    created_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Collection field', 'created')
    )
    modified_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Collection field', 'modified')
    )
    thumbnail_url = models.URLField(
        verbose_name=pgettext_lazy('Collection field', 'thumbnail url')
    )
    videos = models.ManyToManyField(
        Video,
        verbose_name=pgettext_lazy('Collection field', 'videos'),
        blank=True
    )

    objects = CollectionManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @property
    def html_thumbnail(self):
        """ HTML thumbnail image """
        return '<img src="%(thumbnail_url)s" />' % {
            'thumbnail_url': self.thumbnail_url,
        }

    @classmethod
    def import_from_vimeo_object(cls, v_obj):
        """
        Creates or updates one Collection instance with the data from a Vimeo object

        :param v_obj: the Vimeo object
        :return: a tuple (obj, created), where created is a boolean specifying whether an object was created
            and obj is the object
        """
        uri = v_obj['uri']

        if v_obj['pictures'] is not None:
            thumbnail_url = v_obj['pictures']['sizes'][0]['link']
        else:
            thumbnail_url = ''

        obj, created = cls.objects.update_or_create(
            uri=uri,
            defaults={
                'name': v_obj['name'],
                'description': v_obj['description'],
                'url': v_obj['link'],
                'created_datetime': v_obj['created_time'],
                'modified_datetime': v_obj['modified_time'],
                'thumbnail_url': thumbnail_url,
            }
        )

        return obj, created

    def import_videos_from_vimeo(self):
        """
        Import the Videos of the Collection from Vimeo

        :return: a boolean specifying if the videos have been imported or not
        """
        try:
            v_collection_obj = VimeoManager.get_objects_from_vimeo(self.uri)
        except VimeoException:
            return False

        if v_collection_obj['metadata']['connections']['videos']['total'] > 0:
            try:
                v_video_objs = VimeoManager.get_objects_from_vimeo(v_collection_obj['metadata']['connections']['videos']['uri'])
            except VimeoException:
                return False

            for v_video_obj in v_video_objs:
                # Import Video
                video = Video.import_from_vimeo_object(v_video_obj)
                # Add Video to Collection
                self.videos.add(video)

        return True

    def export_to_vimeo(self):
        """
        Exports Collection to Vimeo

        :return: a boolean specifying if the Collection has been exported or not
        """
        synchronized = True

        try:
            VimeoManager.patch_object_on_vimeo(self.uri, data={
                'name': self.name,
                'description': self.description,
            })
        except VimeoException:
            synchronized = False

        # Remove old videos and add new videos
        try:
            v_videos = VimeoManager.get_objects_from_vimeo('%(uri)s/videos' % {
                'uri': self.uri,
            })

            v_videos_to_delete = set([x['uri'] for x in v_videos]).difference([x.uri for x in self.videos.all()])
            v_videos_to_add = set([x.uri for x in self.videos.all()]).difference([x['uri'] for x in v_videos])

            for video_uri in list(v_videos_to_delete):
                try:
                    VimeoManager.delete_object_on_vimeo('%(uri)s%(video_uri)s' % {
                        'uri': self.uri,
                        'video_uri': video_uri,
                    })
                except VimeoException:
                    synchronized = False

            for video_uri in list(v_videos_to_add):
                try:
                    VimeoManager.put_object_on_vimeo('%(uri)s%(video_uri)s' % {
                        'uri': self.uri,
                        'video_uri': video_uri,
                    })
                except VimeoException:
                    synchronized = False

        except VimeoException:
            synchronized = False

        self.synchronized = synchronized
        self.save()

        return synchronized
