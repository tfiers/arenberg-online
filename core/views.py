from django.utils import translation
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect #CSRF attack prevention
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from datetime import datetime
import datetime
from pytz import utc
from django.template import RequestContext
from core.models import  User, UserProfile, Event
from core.htmlcalendar import Calendar
from forms import BirthdayEditForm, UserForm, UserProfileForm, UserEditForm, UserProfileEditForm, CustomPasswordChangeForm, AddEventForm, ContactForm
import gc
import os
import calendar
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from honeypot.decorators import check_honeypot
from django.views.decorators.csrf import csrf_exempt #never use this, only used to exempt send mail form in contact which doesn't have anything to do with user data

@csrf_protect
@check_honeypot
def register(request):
    """handles the view of the registration form"""
    if request.method == 'POST':
        uf = UserForm(request.POST)
        upf = UserProfileForm(request.POST, request.FILES)
        if uf.is_valid() * upf.is_valid():
            user = uf.save()
            #birthday event creation easier and shorter by creating object in view because only date_ov_event is in register form
            Event.objects.create(name='{} {}'.format(user.first_name,user.last_name),event_color="4", date_of_event=uf.cleaned_data['birthdate'], birthday_user=user)
            userprofile = upf.save(commit=False)
            userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.last_password_change = datetime.datetime.now(utc) #setting last password change
            userprofile.save()
            #save the m2m relationship field groups, has to be done like this because we first did commit = False
            upf.save_m2m()
            return render_to_response('registration/thanks_register.html', dict(userform=uf, userprofileform=upf), context_instance=RequestContext(request))
    else:
        uf = UserForm()
        upf = UserProfileForm()
    return render_to_response('registration/register.html', dict(form=uf,profileform=upf), context_instance=RequestContext(request))


@csrf_protect
@login_required
def edit(request):
    """handles the view of the edit form, to edit user info"""
    if request.method == 'POST':
        uf = UserEditForm(request.user,request.POST, instance=request.user, prefix='usereditform')
        upf = UserProfileEditForm(request.POST, request.FILES, instance = request.user.userprofile, prefix='userprofileeditform')
        buser = Event.objects.get(birthday_user=request.user)
        ubf = BirthdayEditForm(request.POST,instance=buser, prefix='birthdayeditform')
        if uf.is_valid() * upf.is_valid() * ubf.is_valid():
            #save user, store in variable for later use
            user = uf.save()
            #save birthday form
            ubf.save()
            #save userprofile, commit=False at first to add user
            userprofile = upf.save(commit=False)
            userprofile.associated_user = user #adds the created as associated user for the userprofile
            userprofile.save()
            #save the m2m relationship field groups, has to be done like this because we first did commit = False
            upf.save_m2m() 
            return render(request,'registration/thanks_edit.html')
    else:
        uf = UserEditForm(request.user,instance=request.user,  prefix='usereditform')
        upf = UserProfileEditForm(instance = request.user.userprofile, prefix='userprofileeditform')
        buser = Event.objects.get(birthday_user=request.user)
        ubf = BirthdayEditForm(instance=buser, prefix='birthdayeditform')
    return render_to_response('registration/edit.html', dict(form=uf, profileform=upf, bdform=ubf), context_instance=RequestContext(request)) 



def set_lang(request, lang='nl'):
	if lang not in ('en', 'nl'):
		lang = 'en' #if people modify url to try get another language
	translation.activate(lang)
	request.session[translation.LANGUAGE_SESSION_KEY] = lang
	referer = urlparse(request.META.get('HTTP_REFERER', '/')).path
	# Cut of the first language part of the url.
	if referer.startswith('/en/'):
		referer = referer[3:]
	return HttpResponseRedirect(referer)

def sponsors(request):
	return render(request, 'sponsors.html')

@csrf_exempt #is OK in dit geval, heeft niets te maken met authenticatie en user moet niet ingelogd zijn en toch geeft het csrf error -.-
@check_honeypot
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Subject: "+form.cleaned_data.get("subject")+", name: "+form.cleaned_data.get("name_visitor")+", email: "+form.cleaned_data.get("email_visitor")
            message = form.cleaned_data.get("message")
            send_mail(subject,message,'contact@arenbergorkest.be',['lennart.bulteel@student.kuleuven.be'])
            return HttpResponseRedirect(reverse('contact_sent'))
    else:
        form = ContactForm()

    return render(request,'contact.html',{'form': form})

def contact_sent(request):
    return render(request, 'contact_sent.html')

def home(request):
	return render(request, 'arenbergorkest.html')

def notapproved(request):
    return render(request, 'registration/notapproved.html')

def axed(request):
    return render(request, 'registration/axed.html')

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def repcalendar(request):
    events = Event.objects.filter(date_of_event__gte=datetime.datetime.now()).order_by("date_of_event")
    bdays = Event.objects.filter(event_color=4).order_by("date_of_event")
    return render(request, 'calendar.html',{'events':events,"birthdays":bdays})

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def calendarview_add(request):
    # If this is a POST request we need to process the form data.
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        form = AddEventForm(request.POST)
        # If the data entered is valid, save a new music piece suggestion
        # to the database.
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('calendarview'))

    # If this is a GET request (or any other type of request) we'll create a blank form.
    else:
        form = AddEventForm()

    return render(request,'calendarview_add.html',{'addeventform': form})

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def musicianlist(request,sort=None,order=None):
    with open(os.path.join(settings.CONFIG_DIR, 'google_list.txt')) as f:
        old_list_url = f.read().strip()
    #any case not covered here will cause a 404, any case not in the ..|..|.. at urls.py will cause one too
    if sort == 'fname':
        sort = 'first_name'
    if sort == 'lname':
        sort = 'last_name'
    if sort == 'phone':
        sort = 'phone_number'
    if sort == 'mail':
        sort = 'email'
    us = []
    uup = []
    bd = []
    if sort == "group": #works
        if order == 'reverse':
            userprofiles = sorted(UserProfile.objects.all(), key=lambda t: t.groups_as_string, reverse=True)
        else:
            userprofiles = sorted(UserProfile.objects.all(), key=lambda t: t.groups_as_string)
        iterator = queryset_iterator(userprofiles)
        #if users is a safety measure for if there are no users. queryset iterator cannot handle empty querysets. 
        #will not happen for users, but stays here in case the code is copied and used for bigger dataset.
        if userprofiles: 
            for u in userprofiles: 
                us.append(u.associated_user)
                uup.append(u)
                bdo = Event.objects.filter(birthday_user=u.associated_user)
                bd += bdo 
            zipped = zip(us,uup,bd)
        else:
            zipped=None
    elif sort == "datebirth": #works
        if order == 'reverse':
            events = Event.objects.exclude(birthday_user=None).order_by('-date_of_event')
        else:
            events = Event.objects.exclude(birthday_user=None).order_by('date_of_event')
        iterator = queryset_iterator(events)
        if events: 
            for e in events:
                us.append(e.birthday_user) 
                up = UserProfile.objects.filter(associated_user=e.birthday_user)
                uup += up
                bd.append(e)
            zipped = zip(us,uup,bd)
        else:
            zipped=None
    elif sort in ["first_name", "last_name", "study", "email", "phone_number"] or sort == None:
        #using the iterator here removes the order_by, which defeats the purpose of sorting the table
        if sort != None:
            if order == 'reverse':
                usr = User.objects.all().order_by("-"+sort)
            else:
                usr = User.objects.all().order_by(sort)
        else:
            usr = User.objects.all()
        bs = usr
        for u in usr: 
            us.append(u)
            uup.append(u.userprofile)
            bdo = Event.objects.filter(birthday_user=u) #returns list with one event object
            bd += bdo 
        zipped = zip(us,uup,bd)
    return render(request, 'musicianlist.html', {'old_list_url':old_list_url, 'musicians': zipped,'voornaam':'fname','achternaam':'lname','mail':'mail',
        'nummer':'phone','studie':'study','groepen':'group','datum':'datebirth','sortedattr':sort,'order':order,'reverse':'reverse'},)

#used in musicianlist
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

    WILL GIVE AN ERROR IF QUERYSET IS EMPTY!!!
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


@login_required
def logout(request):
    return render(request, 'registration/thanks_logout.html')

@csrf_protect
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.user.userprofile.last_password_change = datetime.datetime.now(utc)
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
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def calendarview(request, pYear=datetime.datetime.now().year, pMonth=datetime.datetime.now().month):
    """
    Show calendar of events for specified month and year. The pYear and pMonth arguments are taken from regex in urls.py.
    """
    year = int(pYear)
    month = int(pMonth)
    CalendarFromMonth = datetime.date(year, month, 1)
    CalendarToMonth = datetime.date(year, month, calendar.monthrange(year, month)[1])
    events = Event.objects.filter(date_of_event__gte=CalendarFromMonth, date_of_event__lte= CalendarToMonth).order_by("start_hour")
    birthDays = Event.objects.filter(event_color=4,date_of_event__month=month) #get all birthdays in the current month
    cal= Calendar(events,birthDays).formatmonth(year, month)
    previousyear = year
    previousmonth = month - 1
    if previousmonth == 0:
        previousmonth = 12
        previousyear = year - 1
    nextYear = year
    nextMonth = month + 1
    if nextMonth == 13:
        nextMonth = 1
        nextYear = year + 1

    return render(request, 'calendarview.html', {'Calendar' : mark_safe(cal),
                                                       'Month' : month,
                                                       'MonthName' : named_month(month),
                                                       'Year' : year,
                                                       'PreviousMonth' : previousmonth,
                                                       'PreviousMonthName' : named_month(previousmonth),
                                                       'PreviousYear' : previousyear,
                                                       'NextMonth' : nextMonth,
                                                       'NextMonthName' : named_month(nextMonth),
                                                       'NextYear' : nextYear,
                                                   })