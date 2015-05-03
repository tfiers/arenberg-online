# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0017_unsoldpaperticket'),
    ]

    operations = [
    	migrations.RenameModel(
    		old_name="UnsoldPaperTicket",
    		new_name="GivenPaperTicket",
    	),
    ]
