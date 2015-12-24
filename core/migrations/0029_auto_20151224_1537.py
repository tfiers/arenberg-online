# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20151224_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'/home/lennart/Documents/arenbergvenv/arenberg-online/core/media/images/generic_profile_photo.jpg', upload_to=b'images/avatars'),
        ),
    ]
