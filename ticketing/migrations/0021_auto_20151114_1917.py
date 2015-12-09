# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0020_givenpapertickets_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=b'transfer', max_length=8, null=True, blank=True, choices=[(b'transfer', 'Via overschrijving'), (b'cash', 'Aan de kassa')]),
        ),
        migrations.AlterField(
            model_name='standardmarketingpollanswer',
            name='marketing_feedback',
            field=models.TextField(help_text='Voor antwoorden op de vraag: "Hoe heb je van dit concert gehoord?"', blank=True),
        ),
        migrations.AlterField(
            model_name='standardmarketingpollanswer',
            name='referred_member',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Ken je een muzikant en kom je dankzij hem of haar luisteren?', null=True),
        ),
    ]
