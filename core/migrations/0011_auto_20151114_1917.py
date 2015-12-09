# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150524_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'uploads/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='group',
            name='category',
            field=models.CharField(default=b'standard', max_length=14, choices=[(b'standard', 'Standaard'), (b'musical', 'Muzikaal'), (b'project', 'Project')]),
        ),
    ]
