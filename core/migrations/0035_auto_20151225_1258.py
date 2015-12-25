# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20151225_1238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='get_absolute_url',
            new_name='absolute_url',
        ),
        migrations.AddField(
            model_name='event',
            name='board',
            field=models.BooleanField(default=False, help_text='Designates whether the event is for is_board users only.'),
            preserve_default=True,
        ),
    ]
