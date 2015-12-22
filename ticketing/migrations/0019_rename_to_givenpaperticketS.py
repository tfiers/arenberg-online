# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0018_auto_20150503_2121'),
    ]

    operations = [
    	migrations.RenameModel(
    		old_name="GivenPaperTicket",
    		new_name="GivenPaperTickets",
    	),
    ]
