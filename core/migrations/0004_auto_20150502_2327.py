# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150428_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeGroupName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('email_address', models.CharField(help_text=b"If different from a sanitized version of 'name'", max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('category', models.CharField(default=b'standard', max_length=14, choices=[(b'standard', 'Standaard'), (b'musical', 'Muzikaal'), (b'project', 'Project')])),
                ('email_address', models.CharField(help_text=b"If different from a sanitized version of 'name'", max_length=100)),
                ('parents', models.ManyToManyField(related_name=b'children', to='core.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alternativegroupname',
            name='group',
            field=models.ForeignKey(to='core.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(to='core.Group'),
            preserve_default=True,
        ),
    ]
