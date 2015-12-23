# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20151222_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'/static/images/avatar.jpg', upload_to=b'/static/avatars/'),
            preserve_default=True,
        ),
    ]
