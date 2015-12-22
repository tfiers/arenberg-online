# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20151222_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=b'000000000', max_length=15, verbose_name='phone_number'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='study',
            field=models.CharField(default=b'Graduated', max_length=50, verbose_name='study'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='category',
            field=models.CharField(default=b'standard', max_length=14, choices=[(b'standard', 'Standaard'), (b'musical', 'Muzikaal'), (b'project', 'Project')]),
        ),
    ]
