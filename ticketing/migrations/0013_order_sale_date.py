# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0012_auto_20150503_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sale_date',
            field=models.DateTimeField(default=None, null=True, verbose_name=core.models.User, blank=True),
            preserve_default=True,
        ),
    ]
