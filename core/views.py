from django.utils import translation
from django.core.urlresolvers import resolve
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect

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