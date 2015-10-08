# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150503_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='parents',
        ),
        migrations.AddField(
            model_name='group',
            name='children',
            field=models.ManyToManyField(related_name=b'parents', to='core.Group', blank=True),
            preserve_default=True,
        ),
    ]
