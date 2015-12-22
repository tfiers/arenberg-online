from django.utils import translation
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect #protection for forms and logins and such
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.conf import settings 
from datetime import datetime
from pytz import utc
from django.template import RequestContext
from django.http import HttpResponseRedirect
from core.models import Document #needed for fileupload
from core.forms import DocumentForm #needed for fileupload
from forms import UserForm, UserProfileForm, UserEdit, UserProfileEdit #needed for registration
from django.views.decorators.csrf import csrf_exempt

@csrf_protect
def register(request):
    """handles the view of the registration form"""
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = UserProfileForm(request.POST, prefix='userprofile')
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.last_password_change = datetime.now(utc) #setting last password change
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
        ufdata = {'first_name' : request.user.first_name, 'last_name' : request.user.last_name, 'email' : request.user.email}
        upfdata = {'groups' : request.user.userprofile.groups}
        uf = UserEdit(request.user,request.POST, instance=request.user, initial=ufdata, prefix='user')
        upf = UserProfileEdit(request.user,request.POST, instance = request.user.userprofile, initial=upfdata, prefix='userprofile')
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.last_password_change = datetime.now(utc) #setting last password change
            userprofile.save()
            userprofile.groups = upf.cleaned_data["groups"] #adds the groups. doesn't save because it's a m2m relationship. other options: using super() or save_m2m()
            #TODO: send email here, is also commented out in thanks.html
            return render_to_response('registration/thanks_edit.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))
    else:
        ufdata = {'first_name' : request.user.first_name, 'last_name' : request.user.last_name, 'email' : request.user.email}
        upfdata = {'groups' : request.user.userprofile.groups}
        uf = UserEdit(request.user,instance=request.user, initial=ufdata, prefix='user')
        upf = UserProfileEdit(request.user,instance = request.user.userprofile, initial=upfdata,prefix='userprofile')
    return render_to_response('registration/edit.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))

@login_required
def links(request):
    if not request.user.approved:
        return render(request, 'registration/notapproved.html')
    return render(request, 'links.html')



def set_lang(request, lang='nl'):
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

def notapproved(request):
    return render(request, 'registration/notapproved.html')

@login_required
def calendar(request):
    if not request.user.approved:
        return render(request, 'registration/notapproved.html')
    else: #valueerror (calendar returned None instead of httprespons object) if this else is removed
	   return render(request, 'calendar.html')

@login_required
def activities(request):
    if not request.user.approved:
        return render(request, 'registration/notapproved.html')
    else: #valueerror (calendar returned None instead of httprespons object) if this else is removed
       return render(request, 'activities.html')


@login_required
def logout(request):
    return render(request, 'registration/thanks_logout.html')

@csrf_protect
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.user.userprofile.last_password_change = datetime.now(utc)
            form.user.userprofile.save()
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('pass_changed'))
    else:
        form = PasswordChangeForm(user=request.user)
        
    return render(request, 'registration/password_set_form.html', {'form': form})


@login_required
def password_set(request):
	return render(request, 'registration/pass_changed.html')