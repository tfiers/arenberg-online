# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151222_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='study',
            field=models.CharField(max_length=50, verbose_name='study'),
        ),
    ]
