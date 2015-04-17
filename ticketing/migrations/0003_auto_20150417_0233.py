# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0002_performance_price_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='marketing_answers',
        ),
        migrations.AddField(
            model_name='standardmarketingpollanswer',
            name='related_order',
            field=models.OneToOneField(default=0, to='ticketing.Order'),
            preserve_default=False,
        ),
    ]
