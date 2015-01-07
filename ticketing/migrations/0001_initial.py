# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=75, blank=True)),
                ('last_name', models.CharField(max_length=75, blank=True)),
                ('email', models.EmailField(max_length=75)),
                ('date', models.DateTimeField(verbose_name='date of order')),
                ('remarks', models.TextField(verbose_name="remarks, for questions, special requests, answers to 'how did you hear about this?', ...")),
                ('payment_method', models.CharField(default=b'transfer', max_length=8, choices=[(b'transfer', 'Bank transfer'), (b'cash', 'Cash on the spot')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(blank=True)),
                ('starting_time', models.TimeField(blank=True)),
                ('location', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PriceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('price', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(to='ticketing.Order')),
                ('performance', models.ForeignKey(to='ticketing.Performance')),
                ('price_category', models.ForeignKey(to='ticketing.PriceCategory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='performance',
            name='production',
            field=models.ForeignKey(to='ticketing.Production'),
            preserve_default=True,
        ),
    ]
