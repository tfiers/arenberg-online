# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['first_name']},
        ),
    ]
