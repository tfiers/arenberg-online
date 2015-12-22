# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postermap', '0004_poster_production'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='attachment_type',
            field=models.CharField(blank=True, max_length=14, null=True, choices=[(b'brush_and_glue', 'Borstel en lijm'), (b'pushpin', 'Punaises'), (b'tape', 'Plakband'), (b'other', 'Anders')]),
        ),
    ]
