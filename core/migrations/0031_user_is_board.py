# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20151224_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_board',
            field=models.BooleanField(default=False, help_text='Designates whether the user is part of the board and can view board content.', verbose_name='board'),
            preserve_default=True,
        ),
    ]
