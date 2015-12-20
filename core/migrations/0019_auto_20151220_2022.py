# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20151216_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmemail',
            field=models.EmailField(default='ok', max_length=255, verbose_name='confirmemail'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='confirmpassword',
            field=models.CharField(default='ok', max_length=255, verbose_name='confirmpassword'),
            preserve_default=False,
        ),
    ]
