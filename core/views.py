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
from core.models import  User, UserProfile, Event
from core.htmlcalendar import Calendar
# from core.templatetags.event_tags import ContestCalendar
from forms import UserForm, UserProfileForm, UserEditForm, UserProfileEditForm, CustomPasswordChangeForm #needed for registration and edit profile forms
import gc
import datetime
import calendar
from django.utils.safestring import mark_safe


@csrf_protect
def register(request):
    """handles the view of the registration form"""
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        upf = UserProfileForm(request.POST, request.FILES, prefix='userprofile')
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
        uf = UserEditForm(request.user,request.POST, instance=request.user, prefix='user')
        upf = UserProfileEditForm(request.POST, request.FILES, instance = request.user.userprofile, prefix='userprofile')
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            userprofile = upf.save(commit=False)
            userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.last_password_change = datetime.now(utc) #setting last password change
            userprofile.save()
            userprofile.groups = upf.cleaned_data["groups"] #adds the groups. doesn't save because it's a m2m relationship. other options: using super() or save_m2m()
            #TODO: send email here, is also commented out in thanks.html
            return render_to_response('registration/thanks_edit.html', dict(usereditform=uf, userprofileeditform=upf), context_instance=RequestContext(request))
    else:
        uf = UserEditForm(request.user,instance=request.user,  prefix='user')
        upf = UserProfileEditForm(instance = request.user.userprofile, prefix='userprofile')
    return render_to_response('registration/edit.html', dict(usereditform=uf, userprofileeditform=upf), context_instance=RequestContext(request)) 
    #the keys in the dict actually determine the var names you have to use for the forms in the template

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
def repcalendar(request):
    if not request.user.approved:
        return render(request, 'registration/notapproved.html')
    else: #valueerror (calendar returned None instead of httprespons object) if this else is removed
	   return render(request, 'calendar.html')

@login_required
def musicianlist(request):
    if not request.user.approved:
        return render(request, 'registration/notapproved.html')
    #get all users, iterate over that query to 
    us = []
    uup = []
    iterator = queryset_iterator(User.objects.all()) 
    for u in iterator: 
        us.append(u)
        uup.append(u.userprofile)
    zipped = zip(us,uup)
    #ziet er nu zo uit (getest): [(<User: user1>, <UserProfile: User profile for user1>), (<User: user2>, <UserProfile: User profile for user2>),...]
    return render(request, 'musicianlist.html', {'musicians': zipped})


@login_required
def logout(request):
    return render(request, 'registration/thanks_logout.html')

@csrf_protect
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.user.userprofile.last_password_change = datetime.now(utc)
            form.user.userprofile.save()
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('pass_changed'))
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'registration/password_set_form.html', {'form': form})


@login_required
def password_set(request):
	return render(request, 'registration/pass_changed.html')

def queryset_iterator(queryset, chunksize=1000):
    '''''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes. This reduces memory usage for large tables

    Note that the implementation of the iterator does not support ordered query sets.

    Example:
    my_queryset = queryset_iterator(MyItem.objects.all()) for item in my_queryset: item.do_something()
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()

#CALENDAR FUNCTIONS AND VIEWS

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return datetime.date(1900, pMonthNumber, 1).strftime('%B')

def calendarhome(request):
    """
    Show calendar of events this month
    """
    lToday = datetime.datetime.now()
    return calendarview(request, lToday.year, lToday.month)

@login_required
def calendarview(request, pYear=datetime.datetime.now().year, pMonth=datetime.datetime.now().month):
    """
    Show calendar of events for specified month and year
    """
    if not request.user.approved:
        return render(request, 'registration/notapproved.html')
    else:
        lYear = int(pYear)
        lMonth = int(pMonth)
        if request.method == 'GET' and "year" in request.GET and "month" in request.GET:
            m = request.GET["month"]
            y = request.GET["year"]
            if m != None and y != None:
                lYear = request.GET['year']
                lMonth = request.GET['month']
        lCalendarFromMonth = datetime.date(lYear, lMonth, 1)
        lCalendarToMonth = datetime.date(lYear, lMonth, calendar.monthrange(lYear, lMonth)[1])
        lContestEvents = Event.objects.filter(date_of_event__gte=lCalendarFromMonth, date_of_event__lte=lCalendarToMonth)
        lCalendar = Calendar(lContestEvents).formatmonth(lYear, lMonth)
        lPreviousYear = lYear
        lPreviousMonth = lMonth - 1
        if lPreviousMonth == 0:
            lPreviousMonth = 12
            lPreviousYear = lYear - 1
        lNextYear = lYear
        lYearCorrect = lYear
        lNextMonth = lMonth + 1
        if lNextMonth == 13:
            lNextMonth = 1
            lYearCorrect
            lNextYear = lYear + 1
        lYearAfterThis = lYear + 1
        lYearBeforeThis = lYear - 1

        return render(request, 'calendarview.html', {'Calendar' : mark_safe(lCalendar),
                                                           'Month' : lMonth,
                                                           'MonthName' : named_month(lMonth),
                                                           'Year' : lYear,
                                                           'PreviousMonth' : lPreviousMonth,
                                                           'PreviousMonthName' : named_month(lPreviousMonth),
                                                           'PreviousYear' : lPreviousYear,
                                                           'NextMonth' : lNextMonth,
                                                           'NextMonthName' : named_month(lNextMonth),
                                                           'NextYear' : lNextYear,
                                                           'YearBeforeThis' : lYearBeforeThis,
                                                           'YearAfterThis' : lYearAfterThis,
                                                       })