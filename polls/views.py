from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from polls.forms import NewSemesterPoll
from polls.models import NewSemesterAnswer
from django.utils.translation import ugettext_lazy as _


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

	response = render(request, 'new_semester_poll.html', {'form': form})
	# Workaround to correctly translate the value of the submit button in the form.
	response.content = response.content.replace("Submit form", (_("Gaan met die banaan")).encode('utf-8'))
	return response

def thanks(request):
	return render(request, 'thanks.html')
