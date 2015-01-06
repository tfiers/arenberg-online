from django.contrib import admin
from core.models import User
import django.contrib.auth.admin

class UserAdmin(django.contrib.auth.admin.UserAdmin):
	"""
	See superclass source code:
	https://github.com/django/django/blob/master/django/contrib/auth/admin.py#L40
	"""
	# TODO: Check 'fieldsets' and 'add_fieldsets' in source code: they still contain 'username'
	list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login')
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)