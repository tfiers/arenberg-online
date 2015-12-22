# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0013_order_sale_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardmarketingpollanswer',
            name='marketing_feedback',
            field=models.TextField(help_text='For answers to the question: "How did you hear about this concert?"', blank=True),
        ),
        migrations.AlterField(
            model_name='standardmarketingpollanswer',
            name='referred_member',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Do you know a musician and are you coming because of him or her?', null=True),
        ),
    ]
