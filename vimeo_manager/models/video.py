# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import pgettext_lazy

from ..utils import VimeoManager, VimeoException
from .resource import Resource

# Python 2 fallback
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


@python_2_unicode_compatible
class Video(Resource):
    endpoint = '/me/videos'

    APPROVAL_STATUS_NOT_SUBMITTED = 'N'
    APPROVAL_STATUS_PENDING = 'P'
    APPROVAL_STATUS_APPROVED = 'A'
    APPROVAL_STATUS_REJECTED = 'R'
    APPROVAL_STATUS_CHOICES = (
        (APPROVAL_STATUS_NOT_SUBMITTED, pgettext_lazy('Video approval status choice', 'not submitted')),
        (APPROVAL_STATUS_PENDING, pgettext_lazy('Video approval status choice', 'pending')),
        (APPROVAL_STATUS_APPROVED, pgettext_lazy('Video approval status choice', 'approved')),
        (APPROVAL_STATUS_REJECTED, pgettext_lazy('Video approval status choice', 'rejected')),
    )

    approval_status = models.CharField(
        verbose_name=pgettext_lazy('Video field', 'approval status'),
        max_length=1, choices=APPROVAL_STATUS_CHOICES, default=APPROVAL_STATUS_NOT_SUBMITTED
    )

    # Vimeo properties
    name = models.CharField(
        verbose_name=pgettext_lazy('Video field', 'name'),
        max_length=100
    )
    description = models.TextField(
        verbose_name=pgettext_lazy('Video field', 'description'),
        null=True, blank=True
    )
    url = models.URLField(
        verbose_name=pgettext_lazy('Video field', 'url')
    )
    created_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Video field', 'created')
    )
    modified_datetime = models.DateTimeField(
        verbose_name=pgettext_lazy('Video field', 'modified')
    )
    tags = models.CharField(
        verbose_name=pgettext_lazy('Video field', 'tags'),
        blank=True, max_length=300,
        help_text=pgettext_lazy('Video field tags help', 'Up to 20 keywords, separated by commas')
    )
    thumbnail_url = models.URLField(
        verbose_name=pgettext_lazy('Video field', 'thumbnail url')
    )

    class Meta:
        verbose_name = pgettext_lazy('Video model', 'video')
        verbose_name_plural = pgettext_lazy('Video model', 'videos')

    def __str__(self):
        return self.name

    @property
    def html_link(self):
        """ HTML link to video """
        return '<a target="_blank" href="%(url)s">%(url)s</a>' % {
            'url': self.url,
        }

    @property
    def html_thumbnail(self):
        """ HTML thumbnail image """
        return '<img src="%(thumbnail_url)s" />' % {
            'thumbnail_url': self.thumbnail_url,
        }

    @property
    def html_video_embed(self):
        """ HTML video embed and link to video """
        return '<iframe ' \
               '    src="https://player.vimeo.com/video/%(vimeo_id)s?badge=0&autopause=0&player_id=0" ' \
               '    frameborder="0" ' \
               '    webkitallowfullscreen mozallowfullscreen allowfullscreen>' \
               '</iframe>' \
               '<br />' \
               '%(html_link)s' % {
                   'vimeo_id': self.vimeo_id,
                   'html_link': self.html_link,
               }

    @classmethod
    def import_from_vimeo_object(cls, v_obj):
        """
        Creates or updates one Video instance with the data from a Vimeo object

        :param v_obj: the Vimeo object
        :return: a tuple (obj, created), where created is a boolean specifying whether an object was created
            and obj is the object
        """
        uri = v_obj['uri']
        tags = ', '.join([x['tag'] for x in v_obj['tags']])
        obj, created = cls.objects.update_or_create(
            uri=uri,
            defaults={
                'name': v_obj['name'],
                'description': v_obj['description'],
                'url': v_obj['link'],
                'created_datetime': v_obj['created_time'],
                'modified_datetime': v_obj['modified_time'],
                'tags': tags,
                'thumbnail_url': v_obj['pictures']['sizes'][0]['link'],
            }
        )

        return obj, created

    def export_to_vimeo(self):
        """
        Exports Video to Vimeo

        :return: a boolean specifying if the Video has been exported or not
        """
        synchronized = True
        tags = [x.strip() for x in self.tags.split(',')]

        try:
            VimeoManager.patch_object_on_vimeo(self.uri, data={
                'name': self.name,
                'description': self.description,
            })
        except VimeoException:
            synchronized = False

        # Remove old tags and add new tags
        try:
            v_tags = VimeoManager.get_objects_from_vimeo('%(uri)s/tags' % {
                'uri': self.uri,
            })

            v_tags_to_delete = set([x['name'] for x in v_tags]).difference([x for x in tags])
            v_tags_to_add = set([x for x in tags]).difference([x['name'] for x in v_tags])

            try:
                for tag_name in list(v_tags_to_delete):
                    VimeoManager.delete_object_on_vimeo('%(uri)s/tags/%(tag_name)s' % {
                        'uri': self.uri,
                        'tag_name': tag_name,
                    })
            except VimeoException:
                synchronized = False

            try:
                for tag_name in list(v_tags_to_add):
                    VimeoManager.put_object_on_vimeo('%(uri)s/tags/%(tag_name)s' % {
                        'uri': self.uri,
                        'tag_name': tag_name,
                    })
            except VimeoException:
                synchronized = False
        except VimeoException:
            synchronized = False

        self.synchronized = synchronized
        self.save()

        return synchronized
