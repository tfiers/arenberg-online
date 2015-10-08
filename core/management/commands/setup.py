from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
	args = 'none'
	help = "Executes various setup tasks for the apps in this project."

	def handle(self, *args, **options):
		call_command('migrate_users_from_drupal')
		call_command('setup_groups')
		call_command('setup_space_ticketing')
		# self.stdout.write("Succesfully set-up arenberg-online web app.")