# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0020_givenpapertickets_count'),
        ('postermap', '0003_auto_20150430_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='poster',
            name='production',
            field=models.ForeignKey(to='ticketing.Production', null=True),
            preserve_default=True,
        ),
    ]
