# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0005_standardmarketingpollanswer_related_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standardmarketingpollanswer',
            old_name='related_order',
            new_name='associated_order',
        ),
    ]
