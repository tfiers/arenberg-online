# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20151222_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsemester',
            name='name',
        ),
    ]
