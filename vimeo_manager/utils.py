# -*- coding: utf-8 -*-

import vimeo
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import pgettext_lazy

# Python 2 fallback
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class VimeoException(Exception):
    """ Exception for Vimeo request failure """
    def __init__(self, status_code, uri):
        self.message = 'Error %(status_code)s on %(uri)s' % {
            'status_code': status_code,
            'uri': uri,
        }

    def __str__(self):
        return self.message


class VimeoManager(object):
    vc = vimeo.VimeoClient(
        token=settings.VIMEO_ACCESS_TOKEN,
        key=settings.VIMEO_CLIENT_ID,
        secret=settings.VIMEO_CLIENT_SECRET
    )

    @classmethod
    def get_objects_from_vimeo(cls, uri):
        """
        Returns objects from Vimeo

        :param uri: a Vimeo URI
        :returns one Vimeo object or a list of Vimeo objects
        """
        last_page = False
        data = []
        url = uri

        while not last_page:
            request = cls.vc.get(url)

            if request.status_code != 200:
                raise VimeoException(request.status_code, uri)

            json = request.json()

            # Multiple objects
            if 'data' in json:
                data.extend(json['data'])
            # One object
            else:
                data = json
                break

            if not json['paging']['next']:
                last_page = True
            else:
                url = json['paging']['next']

        return data

    @classmethod
    def delete_object_on_vimeo(cls, uri):
        """ Deletes an object on Vimeo """
        request = cls.vc.delete(uri)

        if request.status_code != 204:
            raise VimeoException(request.status_code, uri)

    @classmethod
    def patch_object_on_vimeo(cls, uri, data=None):
        """ Patches an object on Vimeo """
        request = cls.vc.patch(uri, data=data)

        if request.status_code != 200:
            raise VimeoException(request.status_code, uri)

    @classmethod
    def put_object_on_vimeo(cls, uri, data=None):
        """ Puts an object on Vimeo """
        request = cls.vc.put(uri, data=data)

        if request.status_code != 200:
            raise VimeoException(request.status_code, uri)


def send_video_approval_request_email(request, videos):
    try:
        approval_group = Group.objects.get(name='Approval')
    except Group.DoesNotExist:
        messages.error(request, pgettext_lazy('Video approval', 'Approval group does not exist'))
        return False

    site = Site.objects.get_current()

    email_context = {
        'videos': videos,
        'domain': site.domain,
    }
    html_content = render_to_string(
        'vimeo_manager/emails/video_approval_request_email.html',
        email_context,
    )
    text_content = render_to_string(
        'vimeo_manager/emails/video_approval_request_email.txt',
        email_context,
    )
    subject = pgettext_lazy('Video approval request email', '[%(site_name)s] Video approval request') % {
        'site_name': site.name
    }

    sender = settings.DEFAULT_FROM_EMAIL

    users = User.objects.filter(groups__in=[approval_group])
    recipients = [o.email for o in users]

    msg = EmailMultiAlternatives(subject, text_content, sender, recipients)
    msg.attach_alternative(html_content, 'text/html')
    sent = msg.send()
    return sent
