from django.utils import translation
from django.core.urlresolvers import resolve
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.http import HttpResponse

def set_lang(request, lang='en'):
	if lang not in ('en', 'nl'):
		lang = 'en'
	translation.activate(lang)
	request.session[translation.LANGUAGE_SESSION_KEY] = lang
	referer = urlparse(request.META.get('HTTP_REFERER', '/')).path
	# Cut of the first language part of the url.
	if referer.startswith('/en/') or referer.startswith('/nl/'):
		referer = '/'+referer[4:]
	# return HttpResponse("Ref: {}".format( referer ))
	return HttpResponseRedirect(referer)