# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0004_remove_standardmarketingpollanswer_related_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardmarketingpollanswer',
            name='related_order',
            field=models.OneToOneField(default=1, to='ticketing.Order'),
            preserve_default=False,
        ),
    ]
