# -*- coding: utf-8 -*-

import datetime

from django.contrib.auth.models import Group, User
from django.test import TestCase

from ..models.video import Video
from ..utils import VimeoManager, VimeoException, \
    send_video_approval_request_email


class VimeoManagerTestCase(TestCase):
    def setUp(self):
        self.endpoint = Video.endpoint

    def test_get_objects_from_vimeo_multiple_objects(self):
        """ Returns multiple Vimeo objects """
        try:
            data = VimeoManager.get_objects_from_vimeo(self.endpoint)
        except VimeoException:
            data = None
        self.assertIs(type(data), list)

    def test_get_objects_from_vimeo_one_object(self):
        """ Returns one Vimeo object """
        # Get all objects
        all_objects = VimeoManager.get_objects_from_vimeo(self.endpoint)

        try:
            # Get the first object
            data = VimeoManager.get_objects_from_vimeo(all_objects[0]['uri'])
        except VimeoException:
            data = None
        self.assertIs(type(data), dict)


class UtilsTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='Approval')
        user = User.objects.create_user(username='test')
        user.groups.add(self.group)
        Video.objects.create(
            uri='/uri',
            name='name',
            description='description',
            url='http://example.com',
            created_datetime=datetime.datetime.now(),
            modified_datetime=datetime.datetime.now(),
            thumbnail_url='http://example.com',
        )
        self.videos = Video.objects.all()

    def test_send_video_approval_request_email(self):
        """ Sends a video approval request email """
        sent = send_video_approval_request_email(None, self.videos)
        self.assertGreater(sent, 0)
