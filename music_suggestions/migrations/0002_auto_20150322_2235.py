# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_suggestions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieceofmusic',
            name='link_to_recording',
            field=models.URLField(unique=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pieceofmusic',
            name='sheet_music',
            field=models.TextField(blank=True),
        ),
    ]
