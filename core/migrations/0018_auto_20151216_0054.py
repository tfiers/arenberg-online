# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20151216_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='approved',
            field=models.BooleanField(default=False, help_text='Designates whether this user is approved and may view the login only content.', verbose_name='approved'),
        ),
    ]
