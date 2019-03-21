# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import Group


def create_approval_group(apps, schema_editor):
    Group.objects.get_or_create(name='Approval')


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('synchronized', models.BooleanField(default=True, verbose_name='synchronized')),
                ('last_import_datetime', models.DateTimeField(null=True, verbose_name='last import', blank=True)),
                ('last_export_datetime', models.DateTimeField(null=True, verbose_name='last export', blank=True)),
                ('uri', models.CharField(max_length=50, verbose_name='uri')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(verbose_name='url')),
                ('created_datetime', models.DateTimeField(verbose_name='created')),
                ('modified_datetime', models.DateTimeField(verbose_name='modified')),
                ('thumbnail_url', models.URLField(verbose_name='thumbnail url')),
            ],
            options={
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('synchronized', models.BooleanField(default=True, verbose_name='synchronized')),
                ('last_import_datetime', models.DateTimeField(null=True, verbose_name='last import', blank=True)),
                ('last_export_datetime', models.DateTimeField(null=True, verbose_name='last export', blank=True)),
                ('uri', models.CharField(max_length=50, verbose_name='uri')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(verbose_name='url')),
                ('created_datetime', models.DateTimeField(verbose_name='created')),
                ('modified_datetime', models.DateTimeField(verbose_name='modified')),
                ('thumbnail_url', models.URLField(verbose_name='thumbnail url')),
            ],
            options={
                'verbose_name': 'channel',
                'verbose_name_plural': 'channels',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('synchronized', models.BooleanField(default=True, verbose_name='synchronized')),
                ('last_import_datetime', models.DateTimeField(null=True, verbose_name='last import', blank=True)),
                ('last_export_datetime', models.DateTimeField(null=True, verbose_name='last export', blank=True)),
                ('uri', models.CharField(max_length=50, verbose_name='uri')),
                ('approval_status', models.CharField(default=b'N', max_length=1, verbose_name='approval status', choices=[(b'N', 'not submitted'), (b'P', 'pending'), (b'A', 'approved'), (b'R', 'rejected')])),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(verbose_name='url')),
                ('created_datetime', models.DateTimeField(verbose_name='created')),
                ('modified_datetime', models.DateTimeField(verbose_name='modified')),
                ('tags', models.CharField(help_text='Up to 20 keywords, separated by commas', max_length=300, verbose_name='tags', blank=True)),
                ('thumbnail_url', models.URLField(verbose_name='thumbnail url')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
            },
        ),
        migrations.AddField(
            model_name='channel',
            name='videos',
            field=models.ManyToManyField(to='vimeo_manager.Video', verbose_name='videos', blank=True),
        ),
        migrations.AddField(
            model_name='album',
            name='videos',
            field=models.ManyToManyField(to='vimeo_manager.Video', verbose_name='videos', blank=True),
        ),

        migrations.RunPython(create_approval_group),
    ]
