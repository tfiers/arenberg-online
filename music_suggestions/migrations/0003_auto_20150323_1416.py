# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('music_suggestions', '0002_auto_20150322_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieceofmusic',
            name='suggested_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
