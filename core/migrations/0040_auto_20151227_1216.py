# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_event_end_hour'),
    ]

    operations = [
        migrations.CreateModel(
            name='Birthday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.OneToOneField(to='core.Event')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_color',
            field=models.CharField(default=b'1', help_text='Color code on calendar. Default (1) is red (rehearsal). 2 = concert, 3 = organised event, 4 = birthday, 5 = repetitieweekend.', max_length=1),
        ),
    ]
