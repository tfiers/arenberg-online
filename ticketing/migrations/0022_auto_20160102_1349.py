# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0021_auto_20151222_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
