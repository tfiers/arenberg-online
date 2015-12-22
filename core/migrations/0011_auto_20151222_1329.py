# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150524_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'uploads/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='approved',
            field=models.BooleanField(default=False, help_text='Designates whether this user is approved and may view the login only content.', verbose_name='approved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='associated_user',
            field=models.OneToOneField(null=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(to=b'core.Group'),
        ),
    ]
