# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151211_0119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='associated_user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='groups',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='user',
            name='instrumentgroups',
            field=models.ManyToManyField(to='core.Group', blank=True),
            preserve_default=True,
        ),
    ]
