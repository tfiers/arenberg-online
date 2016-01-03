# coding: utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete
from core.models import User, UserProfile, Group, AlternativeGroupName
from django.conf import settings 
from subprocess import call
import re
from unidecode import unidecode

import requests
from django.conf import settings

#SIGNALS LOOK FOR CHANGES IN CODE ELSEWHERE, AND DO SOMETHING WHEN THEY DETECT THE CHANGE THEY'RE LOOKING FOR
#USED FOR MAILING WITH MAILGUN
#SOME OF MAILING IS DONE IN CORE/VIEWS.PY BECAUSE IT WAS EASIER THERE (because of m2m relationship groups)
#THAT DOES MEAN THAT, ATM, EDITING GROUPS OR MAIL ADRESSES OF USERS/USERPROFILES (in django admin) DO NOT UPDATE MAILING LISTS!!!

@receiver(post_save, sender=Group)
def create_mailing_list_group(sender, instance, **kwargs):
	"""
	Detects when a Group is created, and automatically creates a mailing list in Mailgun to go with the group.
	"""
	name = instance.name
	return requests.post("https://api.mailgun.net/v3/lists",
        auth=('api', settings.MAILGUN_API_KEY),
        data={'address': '{}@arenbergorkest.be'.format(name),
              'description': name})

@receiver(post_delete, sender=Group)
def remove_mailing_list_group(sender, instance, **kwargs):
	"""
	Detects when a Group is deleted, and automatically removes the mailing list in Mailgun.
	"""
	name = instance.name
	return requests.delete("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be".format(name),auth=('api', settings.MAILGUN_API_KEY))