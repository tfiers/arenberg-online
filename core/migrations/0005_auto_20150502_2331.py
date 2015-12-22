# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150502_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='email_address',
            field=models.CharField(help_text=b"If different from a sanitized version of 'name'", max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='parents',
            field=models.ManyToManyField(related_name=b'children', to=b'core.Group', blank=True),
        ),
    ]
