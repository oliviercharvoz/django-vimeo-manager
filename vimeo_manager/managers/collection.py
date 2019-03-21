# -*- coding: utf-8 -*-

from .resource import ResourceManager


class CollectionManager(ResourceManager):
    def update_and_import_videos_from_vimeo(self):
        """
        Updates the Collection instances in the queryset with the data from Vimeo
        and imports the related Videos

        :return: a boolean specifying if the Collection instances have been updated or not
        """
        updated = True

        for collection in self.get_queryset():
            collection_updated = collection.update_from_vimeo()

            if collection_updated:
                video_updated = collection.import_videos_from_vimeo()

                if not video_updated:
                    updated = False
            else:
                updated = False

        return updated
