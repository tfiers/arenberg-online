# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitutde', models.FloatField()),
                ('longitude', models.FloatField()),
                ('hanging_date', models.DateTimeField()),
                ('for_what_id', models.PositiveSmallIntegerField()),
                ('location_name', models.CharField(max_length=400, blank=True)),
                ('count', models.PositiveSmallIntegerField(default=1)),
                ('entered_on', models.DateTimeField(null=True, blank=True)),
                ('remarks', models.TextField(blank=True)),
                ('attachment_type', models.CharField(blank=True, max_length=8, choices=[(b'brush_and_glue', 'Borstel en lijm'), (b'pushpin', 'Punaises'), (b'tape', 'Plakband'), (b'other', 'Anders')])),
                ('entered_by', models.ForeignKey(related_name=b'entered_posters', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('for_what_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('hung_by', models.ManyToManyField(related_name=b'hung_posters', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
