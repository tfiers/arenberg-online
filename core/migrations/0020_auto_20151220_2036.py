# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20151220_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmemail',
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmpassword',
        ),
    ]
