# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_contestevent_get_absolute_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_event', models.DateField(default=datetime.date.today, max_length=50)),
                ('name', models.CharField(default=b'Repetitie', max_length=20)),
                ('location', models.CharField(default=b'STUK', max_length=20)),
                ('start_hour', models.TimeField(default=datetime.time(20, 0))),
                ('get_absolute_url', models.CharField(default=b'', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='ContestEvent',
        ),
    ]
