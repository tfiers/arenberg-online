# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150502_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternativegroupname',
            name='email_address',
            field=models.CharField(help_text=b"If different from a sanitized version of 'name'", max_length=100, blank=True),
        ),
    ]
