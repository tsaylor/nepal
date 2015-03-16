# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('profile_id', models.BigIntegerField(db_index=True)),
                ('screen_name', models.CharField(max_length=45, db_index=True)),
                ('name', models.CharField(max_length=45)),
                ('location', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=200)),
                ('profile_image_url', models.URLField()),
                ('oauth_token', models.CharField(max_length=200)),
                ('oauth_token_secret', models.CharField(max_length=200)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status_id', models.BigIntegerField(db_index=True)),
                ('text', models.CharField(max_length=200)),
                ('_status_json', models.TextField(blank=True)),
                ('profile', models.ForeignKey(to='profiles.Profile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
