# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_suggestions', '0003_auto_20150323_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='pieceofmusic',
            name='suggested_by_string',
            field=models.CharField(default='', max_length=200, blank=True),
            preserve_default=False,
        ),
    ]
