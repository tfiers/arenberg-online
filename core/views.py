from django.utils import translation
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect #protection for forms and logins and such
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.conf import settings 
from datetime import datetime
from pytz import utc
from django.template import RequestContext
from django.http import HttpResponseRedirect
from core.models import Document #needed for fileupload
from core.forms import DocumentForm #needed for fileupload
from forms import UserForm, UserProfileForm, UserFormUpdate, UserProfileFormUpdate #needed for registration
from django.views.decorators.csrf import csrf_exempt

@csrf_protect
def register(request):
    """handles the view of the registration form"""
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = UserProfileForm(request.POST, prefix='userprofile')
        if uf.is_valid() * upf.is_valid():
            user = uf.saveTotal()
            userprofile = upf.save(commit=False)
            userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.save()
            userprofile.groups = upf.cleaned_data["groups"] #adds the groups. doesn't save because it's a m2m relationship. other options: using super() or save_m2m()
            #TODO: send email here, is also commented out in thanks.html
            return render_to_response('registration/thanks_register.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))
    else:
        uf = UserForm(prefix='user')
        upf = UserProfileForm(prefix='userprofile')
    return render_to_response('registration/register.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))

@csrf_protect
@login_required
def edit(request):
    """handles the view of the edit form, to edit user info"""
    if request.method == 'POST':
        uf = UserFormUpdate(request.POST, user=request.user, instance=request.user,prefix='user')
        upf = UserProfileFormUpdate(request.POST, instance=request.user.userprofile,prefix='userprofile')
       
        uf.data = uf.data.copy()
        upf.data = upf.data.copy()
        #deleting empty fiels, they won't be updated
        if request.POST.get('first_name', False) == False:
            uf.data.pop("first_name", None)
        if request.POST.get('last_name', False) == False:
            uf.data.pop("last_name", None)
        if request.POST.get('password', False) == False: 
            uf.data.pop("password", None)
        if request.POST.get('groups', False) == False:
            uf.data.pop("groups", None)      
        
        if uf.is_valid() * upf.is_valid():
            user = uf.saveTotal()
            # userprofile = upf.save(commit=False)
            # userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.save()
            userprofile.groups = upf.cleaned_data["groups"] #adds the groups. doesn't save before because it's a m2m relationship. other options: using super() or save_m2m()
            #TODO: send email here, is also commented out in thanks.html
            return render_to_response('registration/thanks_edit.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))
    else:
        uf = UserFormUpdate(prefix='user')
        upf = UserProfileFormUpdate(prefix='userprofile')
    return render_to_response('registration/edit.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))

@login_required
def list(request):
    """handles file upload"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('arenberg-online.core.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

@login_required
def links(request):
    return render(request, 'links.html')



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

def sponsors(request):
	return render(request, 'sponsors.html')

def contact(request):
	return render(request, 'contact.html')

def home(request):
	return render(request, 'Arenbergorkest.htm')

@login_required
def calendar(request):
	return render(request, 'calendar.html')

@login_required
def logout(request):
    return render(request, 'registration/thanks_logout.html')

@csrf_protect
@login_required
def change_default_password(request):
	if check_password(settings.DEFAULT_NEW_PASSWORD, request.user.password):
		# User hasn't changed his default password yet.
		if request.method == 'POST':
			form = SetPasswordForm(user=request.user, data=request.POST)
			if form.is_valid():
				return HttpResponseRedirect(reverse('pass_changed'))
		else:
			form = SetPasswordForm(user=request.user)
			
		return render(request, 'registration/password_set_form.html', {'form': form, 'default_pass': settings.DEFAULT_NEW_PASSWORD})
	else:
		return HttpResponseRedirect(reverse('wie'))

@login_required
def password_set(request):
	return render(request, 'registration/pass_changed.html')