from django.core.management.base import BaseCommand

from vimeo_manager.models.video import Video
from vimeo_manager.models.album import Album
from vimeo_manager.models.channel import Channel


class Command(BaseCommand):
    def handle(self, *args, **options):
        Video.import_all_from_vimeo()
        Album.import_all_from_vimeo()
        Channel.import_all_from_vimeo()
