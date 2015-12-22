# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0006_auto_20150417_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='online',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=75, null=True, blank=True),
        ),
    ]
