# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_newsemester_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsemester',
            name='user',
        ),
        migrations.AddField(
            model_name='newsemester',
            name='name',
            field=models.CharField(default=False, max_length=200),
            preserve_default=True,
        ),
    ]
