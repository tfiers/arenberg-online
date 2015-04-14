# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingPollAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=75)),
                ('date', models.DateTimeField(verbose_name='datum van online bestelling')),
                ('payment_method', models.CharField(default=b'transfer', max_length=8, choices=[(b'transfer', 'By bank transfer'), (b'cash', 'Cash at the desk')])),
                ('user_remarks', models.TextField(help_text='opmerkingen gebruiker. Voor vragen en speciale verzoeken.', null=True, blank=True)),
                ('admin_remarks', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, verbose_name='datum en eventueel uur', blank=True)),
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
                'verbose_name_plural': 'price categories',
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
            name='StandardMarketingPollAnswer',
            fields=[
                ('marketingpollanswer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ticketing.MarketingPollAnswer')),
                ('marketing_feedback', models.TextField(help_text='Voor antwoorden op de vraag: "Hoe heb je van dit concert gehoord?"', blank=True)),
                ('first_concert', models.NullBooleanField()),
                ('referred_member', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Ken je een muzikant en kom je dankzij hem of haar luisteren?', null=True)),
            ],
            options={
            },
            bases=('ticketing.marketingpollanswer',),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.ForeignKey(to='ticketing.Order')),
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
        migrations.AddField(
            model_name='order',
            name='marketing_answers',
            field=models.OneToOneField(null=True, blank=True, to='ticketing.MarketingPollAnswer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='performance',
            field=models.ForeignKey(to='ticketing.Performance'),
            preserve_default=True,
        ),
    ]
