# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0014_auto_20150503_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'transfer', max_length=8, blank=True, choices=[(b'transfer', 'By bank transfer'), (b'cash', 'Cash at the desk')]),
        ),
    ]
