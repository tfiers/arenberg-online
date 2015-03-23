# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20150107_0045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricecategory',
            options={'verbose_name_plural': 'price categories'},
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='number',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'transfer', max_length=8, choices=[(b'transfer', 'Via overschrijving'), (b'cash', 'Aan de kassa')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='remarks',
            field=models.TextField(verbose_name="remarks. For questions, special requests, answers to 'how did you hear about this?', ...", blank=True),
        ),
    ]
