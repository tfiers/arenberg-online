# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0009_performance_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='short_name',
        ),
    ]
