=============
Vimeo Manager
=============

Vimeo Manager is a simple Django app that adds a layer on top of Vimeo API.
Currently it allows to edit videos, albums and channels information and collaborate
on video approval.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "vimeo_manager" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'vimeo_manager',
    ]

2. Run `python manage.py migrate` to create the models and the Approval group.

3. Initialize the following constants in your settings.py
   (assuming that you already have Vimeo developer credentials):
    - VIMEO_ACCESS_TOKEN
    - VIMEO_CLIENT_ID
    - VIMEO_CLIENT_SECRET

4. Run `python manage.py import_from_vimeo` to import the data from your Vimeo account.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to manage your Vimeo account (you'll need the Admin app enabled).