# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_auto_20150107_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='remarks',
            field=models.TextField(verbose_name="remarks, for questions, special requests, answers to 'how did you hear about this?', ...", blank=True),
        ),
    ]
