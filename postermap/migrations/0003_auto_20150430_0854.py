# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postermap', '0002_auto_20150428_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poster',
            name='attachment_type',
            field=models.CharField(blank=True, max_length=14, null=True, choices=[(b'brush_and_glue', 'Brush and glue'), (b'pushpin', 'Pushpins'), (b'tape', 'Tape'), (b'other', 'Other')]),
        ),
    ]
