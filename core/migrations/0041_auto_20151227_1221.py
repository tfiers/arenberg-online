# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20151227_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birthday',
            name='event',
        ),
        migrations.RemoveField(
            model_name='birthday',
            name='user',
        ),
        migrations.DeleteModel(
            name='Birthday',
        ),
        migrations.AddField(
            model_name='event',
            name='birthday_user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, help_text='If this event is a birthday, this attr holds the user.'),
            preserve_default=True,
        ),
    ]
