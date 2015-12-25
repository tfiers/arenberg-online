# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20151225_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='absolute_url',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
