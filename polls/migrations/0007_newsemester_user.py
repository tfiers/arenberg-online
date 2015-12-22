# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_remove_newsemester_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsemester',
            name='user',
            field=models.CharField(default=False, max_length=100),
            preserve_default=True,
        ),
    ]
