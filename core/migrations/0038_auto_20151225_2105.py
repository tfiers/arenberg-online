# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20151225_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_color',
            field=models.CharField(default=b'1', help_text='Color code on calendar. Default (1) is red (rehearsal). 2 = concert, 3 = organised event, 4 = birthday.', max_length=1),
        ),
    ]
