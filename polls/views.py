from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from polls.forms import NewSemesterPoll, ZaventemTransportForm
from polls.models import NewSemester, ZaventemTransport
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

def thanks(request):
	return render(request, 'thanks.html')

def new_semester(request):
	if not request.user.approved:
		return HttpResponseRedirect(reverse('notapproved'))
	#prevents UNIQUE constraint failed by filling same form out twice
	if NewSemester.objects.filter(user=request.user):
		return HttpResponseRedirect(reverse('thanks'))
	# If this is a POST request we need to process the form data.
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request:
		form = NewSemesterPoll(request.POST)
		# If the data entered is valid, save a new answer
		# to the database.
		if form.is_valid():
			answer = NewSemester.objects.create(
				user = request.user,
				plans = form.cleaned_data['plans_input'],
				next_semester = form.cleaned_data['next_semester_input'],
				engage = form.cleaned_data['engage_input'],
			)
			return HttpResponseRedirect(reverse('thanks'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = NewSemesterPoll()

	response = render(request, 'new_semester.html', {'form': form})
	# Workaround to correctly translate the value of the submit button in the form.
	response.content = response.content.replace("Submit form", (_("Gaan met die banaan")).encode('utf-8'))
	return response

# @login_required
# def zaventem_transport(request):
# 	if request.method == 'POST':
# 		form = ZaventemTransportForm(request.POST, instance=ZaventemTransport(musician=request.user))
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect(reverse('thanks'))
# 	else:
# 		form = ZaventemTransportForm()

# 	return render(request, 'zaventem_transport.html', {'form': form})