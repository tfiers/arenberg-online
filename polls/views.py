from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from polls.forms import NewSemesterPoll
from polls.models import NewSemesterAnswer


def new_semester_answer(request):
	# If this is a POST request we need to process the form data.
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request:
		form = NewSemesterPoll(request.POST)
		# If the data entered is valid, save a new answer
		# to the database.
		if form.is_valid():
			answer = NewSemesterAnswer.objects.create(
				name = form.cleaned_data['name_input'],
				plans = form.cleaned_data['plans_input'],
				next_semester = form.cleaned_data['next_semester_input'],
				engage = form.cleaned_data['engage_input'],
			)
			return HttpResponseRedirect(reverse('thanks'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = NewSemesterPoll()

	return render(request,
		'new_semester_poll.html',
		{'form': form})

def thanks(request):
	return render(request, 'thanks.html')
