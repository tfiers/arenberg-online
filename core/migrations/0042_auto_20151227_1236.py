# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20151227_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_hour',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_hour',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
