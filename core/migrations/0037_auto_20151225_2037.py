# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20151225_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_color',
            field=models.CharField(default=b'1', help_text='Color code on calendar. Default (1) is red.', max_length=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='absolute_url',
            field=models.CharField(help_text="It's possible to make the event link to a page (opened in a tab).", max_length=100, null=True, blank=True),
        ),
    ]
