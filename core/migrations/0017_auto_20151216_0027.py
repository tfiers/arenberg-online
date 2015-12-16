# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_userprofile_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='approved',
            field=models.BooleanField(default=False, help_text='Designates whether this user is approved and may view the login only content.', verbose_name='active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='category',
            field=models.CharField(default=b'standard', max_length=14, choices=[(b'standard', 'Standard'), (b'musical', 'Musical'), (b'project', 'Project')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(to=b'core.Group'),
        ),
    ]
