# coding: utf-8

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from core.models import User, UserProfile, Group, AlternativeGroupName
from django.conf import settings 
from subprocess import call
import re
from unidecode import unidecode

def remove_space(name):
	return name.replace(" ", "")

def sanitize(name):
	name = name.strip() # Remove leading and trailing whitespace
	name = re.sub(' +', ' ', name) # Remove repeated spaces
	name = name.replace(" ", ".") # Replace spaces with dots
	name = unidecode(name) # Convert e.g. u'é' to 'e'
	name = name.lower() # Lowercase
	return name

@receiver(post_save, sender=User)
@receiver(m2m_changed, sender=UserProfile.groups.through)
@receiver(post_save, sender=Group)
@receiver(post_save, sender=AlternativeGroupName)
def update_email_forwards(sender, instance, **kwargs):
	''' Updates postfix email forwards when a user changes his
		email address, when a user is added to / removed from a group
		, when a group is updated, or when an alternative group
		name is created / updated. '''

	# TODO: only update virtual alias file when:
	#  - User changed email
	#  - UserProfile changed groups
	#  - Group changed name or email (..)
	#  - AlternativeGroupName changed
	# See here: http://stackoverflow.com/a/7934958


	# Add catchall email to postfix virtual aliases file
	c = '{} {}\n'.format('@arenbergorkest.be', settings.CATCHALL_EMAIL)

	# Virtual alias file syntax:
	# email, space, email, (space, email, space, email,) newline, (repeat)
	# Catchall alias email = '@arenbergorkest.be'
	# Example:
	# bestuur@arenbergorkest.be 	jef@gmail.com jos@hotmail.com
	# jef@arenbergokest.be 			jef@gmail.com
	# @arenbergorkest.be 			bestuur@arenbergorkest.be

	# Add email forwards of the form 'gert@arenbergorkest.be'
	# and 'gert.verhulst@arenbergorkest.be'.
	for user in User.objects.all():
		long_address = sanitize(remove_space(user.first_name)+"."+remove_space(user.last_name))
		# Add line to Postfix virtual aliases file.
		c += '{} {}\n'.format(
			long_address+'@arenbergorkest.be', 
			user.email)
		# If there is no other musician with the same first name
		if not User.objects.exclude(id=user.id).filter(first_name=user.first_name).exists():
			short_address = sanitize(user.first_name)
			# Add line to Postfix virtual aliases file.
			c += '{} {}\n'.format(
				short_address+'@arenbergorkest.be', 
				user.email)

	# Add email forwards based on groups.
	for group in Group.objects.all():
		# Search for all Users and their email in this group and its
		# descendant groups.
		destinations = []
		profiles = UserProfile.objects.filter(
			groups__in=group.get_all_descendant_groups(include_self=True))
		for userProfile in profiles:
			destinations.append(userProfile.associated_user.email)

		# Remove duplicates (Users that are in more than one group of a hierarchy)
		destinations = set(destinations)

		# Loop over all email forwarding adresses that should be catched
		alternatives = list(AlternativeGroupName.objects.filter(group=group))
		for g in [group] + alternatives:
			if g.email_address == '':
				email_forwarding_address = g.name
			else:
				email_forwarding_address = g.email_address

			# Add line to Postfix virtual aliases file.
			c += '{} {}\n'.format(
				sanitize(email_forwarding_address)+'@arenbergorkest.be', 
				' '.join(destinations))

	with open(settings.POSTFIX_VIRTUAL_ALIAS_FILE, 'w') as f:
		f.write(c)
	if not settings.DEVELOPPING:
		call(['sudo', 'postmap', settings.POSTFIX_VIRTUAL_ALIAS_FILE])

