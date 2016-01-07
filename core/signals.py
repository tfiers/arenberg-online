from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete, pre_save, pre_delete
from core.models import User, UserProfile, Group
from django.conf import settings 
import requests

@receiver(post_save, sender=Group)
def create_mailing_list_group(sender, instance, **kwargs):
	"""
	Detects when a Group is created, and automatically creates a mailing list in Mailgun to go with the group.
	"""
	name = instance.name
	return requests.post("https://api.mailgun.net/v3/lists",
        auth=('api', settings.MAILGUN_API_KEY),
        data={'address': '{}@arenbergorkest.be'.format(name),
              'name': name})

@receiver(post_delete, sender=Group)
def remove_mailing_list_group(sender, instance, **kwargs):
	"""
	Detects when a Group is deleted, and automatically removes the mailing list in Mailgun.
	"""
	name = instance.name
	return requests.delete("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be".format(name),auth=('api', settings.MAILGUN_API_KEY))

@receiver(m2m_changed,sender=UserProfile.groups.through)
def change_user_mailing_lists(sender, instance, action, reverse, model, pk_set, **kwargs):
	"""
	Detects when something in the m2m relationship of groups and users is changed and applies those changes to the mailing lists.
	"""
	mail = instance.associated_user.email
	username = instance.associated_user.first_name+" "+instance.associated_user.last_name
	#if groups are going to be added
	if action == "post_add":
		groups = instance.groups_as_string
		groups = groups.split(", ")
		#put all added groups_as_string
		for group in groups:
		 	requests.post("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be/members".format(group),
		    auth=('api', settings.MAILGUN_API_KEY),
		    data={'subscribed': True,
		    	  'name':username,
		          'address': mail})
	#if groups are going to be removed
	if action == "pre_clear": 
		#put the removed groups from a set in a list
		previous = UserProfile.objects.get(pk=instance.pk)
		grplst = previous.groups_as_string.split(", ")
		#loop over list
		for grp in grplst:
			requests.delete("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be/members/{}".format(grp,mail),auth=('api', settings.MAILGUN_API_KEY))

@receiver(pre_save, sender=User)
def do_something_if_changed(sender, instance, **kwargs):
	"""
	Changes user mailadresses in all mailing lists he's part of. Only needed in edit: in register change_user_mailing_lists will do the trick.
	"""
	try:
		usr = sender.objects.get(pk=instance.pk) 
	except sender.DoesNotExist:
	    pass #user is new (register) so ignore signal
	else:
		#user exists (edit form), check if mail has changed:
		username = instance.first_name+" "+instance.last_name
		if usr.email != instance.email:
			group_list_usr = usr.userprofile.groups_as_string.split(", ")
			for grp in group_list_usr:
				requests.delete("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be/members/{}".format(grp,usr.email),auth=('api', settings.MAILGUN_API_KEY))
	    	group_list_inst = instance.userprofile.groups_as_string.split(", ")
	    	for gr in group_list_inst:
				requests.post("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be/members".format(gr),
			    auth=('api', settings.MAILGUN_API_KEY),
			    data={'subscribed': True,
			    	  'name':username,
			          'address': instance.email})

@receiver(pre_delete, sender=UserProfile)
def remove_from_earth(sender, instance, **kwargs):
	"""
	Removes a user from all mailing lists when he's deleted, reacts upon UserProfile pre_delete.
	"""
	grplst = instance.groups_as_string.split(", ")
	mail = instance.associated_user.email
	#loop over list
	for grp in grplst:
		requests.delete("https://api.mailgun.net/v3/lists/{}@arenbergorkest.be/members/{}".format(grp,mail),auth=('api', settings.MAILGUN_API_KEY))