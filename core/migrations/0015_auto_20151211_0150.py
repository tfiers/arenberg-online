# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20151211_0144'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old_drupal_uid', models.IntegerField(default=None, null=True, blank=True)),
                ('last_password_change', models.DateTimeField(default=None, null=True, blank=True)),
                ('associated_user', models.OneToOneField(null=True, default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='user',
            name='instrumentgroups',
        ),
    ]
