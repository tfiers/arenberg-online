# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_contestevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestevent',
            name='get_absolute_url',
            field=models.CharField(default=b'http://www.google.com', max_length=100),
            preserve_default=True,
        ),
    ]
