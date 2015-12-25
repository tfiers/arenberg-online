# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_user_is_board'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_event', models.DateField(default=datetime.date.today, max_length=50)),
                ('name', models.CharField(default=b'Repetitie', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
