# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='price_categories',
            field=models.ManyToManyField(to='ticketing.PriceCategory'),
            preserve_default=True,
        ),
    ]
