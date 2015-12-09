# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20150428_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zaventemtransport',
            name='transport',
            field=models.CharField(default=b'group', max_length=5, choices=[(b'group', '.. met de groep'), (b'own', '.. met eigen vervoer')]),
        ),
    ]
