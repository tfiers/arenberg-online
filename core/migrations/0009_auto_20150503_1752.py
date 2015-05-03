# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150503_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='category',
            field=models.CharField(default=b'standard', max_length=14, choices=[(b'standard', 'Standard'), (b'musical', 'Musical'), (b'project', 'Project')]),
        ),
    ]
