# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_remove_user_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_of_event',
            field=models.DateField(max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
