# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20151225_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_hour',
            field=models.TimeField(default=datetime.time(22, 15)),
            preserve_default=True,
        ),
    ]
