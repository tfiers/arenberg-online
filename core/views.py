from django.utils import translation
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.conf import settings 
from datetime import datetime
from pytz import utc

def set_lang(request, lang='en'):
	if lang not in ('en', 'nl'):
		lang = 'en'
	translation.activate(lang)
	request.session[translation.LANGUAGE_SESSION_KEY] = lang
	referer = urlparse(request.META.get('HTTP_REFERER', '/')).path
	# Cut of the first language part of the url.
	if referer.startswith('/en/'):
		referer = referer[3:]
	return HttpResponseRedirect(referer)

def redirect_to_old_drupal_site(request, path='/'):
	return HttpResponseRedirect('http://arenbergorkest.studentenweb.org/'+path)

@csrf_protect
@login_required
def change_default_password(request):
	if check_password(settings.DEFAULT_NEW_PASSWORD, request.user.password):
		# User hasn't changed his default password yet.
		if request.method == 'POST':
			form = SetPasswordForm(user=request.user, data=request.POST)
			if form.is_valid():
				form.user.userprofile.last_password_change = datetime.now(utc)
				form.user.userprofile.save()
				form.save()
				update_session_auth_hash(request, form.user)
				return HttpResponseRedirect(reverse('pass_changed'))
		else:
			form = SetPasswordForm(user=request.user)
			
		return render(request, 'registration/password_set_form.html', {'form': form, 'default_pass': settings.DEFAULT_NEW_PASSWORD})
	else:
		return HttpResponseRedirect(reverse('space_ticketing:musician_tickets'))

@login_required
def password_set(request):
	return render(request, 'registration/pass_changed.html')