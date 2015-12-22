# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewSemesterAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('plans', models.TextField(blank=True)),
                ('next_semester', models.BooleanField()),
                ('engage', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
