# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_suggestions', '0004_pieceofmusic_suggested_by_string'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pieceofmusic',
            options={'ordering': ['-id'], 'verbose_name_plural': 'pieces of music'},
        ),
    ]
