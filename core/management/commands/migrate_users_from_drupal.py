from django.core.management.base import BaseCommand
from core.models import User, UserProfile
from user_list import user_list
from django.conf import settings

class Command(BaseCommand):
	args = 'none'
	help = ("Creates users based on emails and names of the old Drupal system, "
			"giving them a default password.")

	def handle(self, *args, **options):
		for line in user_list:
			old_drupal_uid, first_name, last_name, email = line
			if not User.objects.filter(email=email).exists():
				user = User.objects.create_user(
					email=email,
					first_name=first_name,
					last_name=last_name,
					password=settings.DEFAULT_NEW_PASSWORD,
				)
				profile = UserProfile.objects.create(
					associated_user=user,
					old_drupal_uid=old_drupal_uid,
				)
		self.stdout.write("Succesfully migrated users.")
