# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20150417_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standardmarketingpollanswer',
            name='related_order',
        ),
    ]
