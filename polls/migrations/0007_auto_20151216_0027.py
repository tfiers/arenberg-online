# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20151114_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zaventemtransport',
            name='transport',
            field=models.CharField(default=b'group', max_length=5, choices=[(b'group', '.. with the group'), (b'own', '.. by myself')]),
        ),
    ]
