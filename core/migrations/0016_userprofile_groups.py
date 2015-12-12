# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20151211_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(to='core.Group', blank=True),
            preserve_default=True,
        ),
    ]
