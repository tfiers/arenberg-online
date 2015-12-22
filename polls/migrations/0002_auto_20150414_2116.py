# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsemesteranswer',
            name='engage',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='newsemesteranswer',
            name='next_semester',
            field=models.BooleanField(default=False),
        ),
    ]
