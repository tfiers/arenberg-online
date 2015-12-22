# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0003_auto_20150425_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZaventemTransport',
            fields=[
                ('pollanswer_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='polls.PollAnswer')),
                ('transport', models.CharField(default=b'group', max_length=5, choices=[(b'group', '.. met de groep'), (b'own', '.. met eigen vervoer')])),
                ('musician', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=('polls.pollanswer',),
        ),
    ]
