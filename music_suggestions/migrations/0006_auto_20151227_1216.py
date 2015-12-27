# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_suggestions', '0005_auto_20150329_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pieceofmusic',
            name='sheet_music',
            field=models.TextField(null=True, blank=True),
        ),
    ]
