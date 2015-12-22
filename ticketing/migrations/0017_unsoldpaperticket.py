# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('ticketing', '0016_auto_20150503_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnsoldPaperTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('given_on', models.DateTimeField(null=True, blank=True)),
                ('for_what_id', models.PositiveSmallIntegerField()),
                ('for_what_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('given_to', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
