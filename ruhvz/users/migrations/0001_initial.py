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
                ('activation_key', models.CharField(max_length=40, null=True, blank=True)),
                ('activation_key_expires', models.DateTimeField(null=True, blank=True)),
                ('last_words', models.CharField(max_length=255, blank=True)),
                ('subscribe_death_notifications', models.BooleanField(default=False)),
                ('subscribe_chatter_listhost', models.BooleanField(default=True)),
                ('subscribe_zombies_listhost', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
