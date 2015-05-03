# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0008_order_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='short_name',
            field=models.CharField(default=b'', max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
