# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150414_2116'),
    ]

    operations = [
    	migrations.RenameModel('NewSemesterAnswer', 'NewSemester'),
    ]
