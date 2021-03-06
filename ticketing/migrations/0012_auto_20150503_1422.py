# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0011_performance_short_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricecategory',
            old_name='name',
            new_name='full_name',
        ),
        migrations.AddField(
            model_name='pricecategory',
            name='short_name',
            field=models.CharField(default=b'', max_length=30, blank=True),
            preserve_default=True,
        ),
    ]
