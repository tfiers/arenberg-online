# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20151222_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(default=datetime.date.today, max_length=50, verbose_name='study'),
            preserve_default=True,
        ),
    ]
