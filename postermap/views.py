from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from postermap.models import Poster
from ticketing.models import Production
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, ChoiceField, DateTimeField
from datetime import datetime
from pytz import utc

class PosterForm(ModelForm):
	attachment_type = ChoiceField(choices=Poster.attachment_type_choices, required=False)
	class Meta:
		model = Poster
		fields = ['latitude', 'longitude', 'hanging_date', 'location_name', 
				  'count', 'hung_by', 'remarks', 'attachment_type']

@login_required
def add_space_poster(request):
	if request.method == 'POST':
		form = PosterForm(request.POST, instance=Poster(
			entered_by=request.user, entered_on=datetime.now(utc),
			for_what=Production.objects.get(name="S P A C E - Lente 2015")))
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('space_ticketing:space_posters'))
	else:
		form = PosterForm(initial={'hanging_date': datetime.now().strftime('%Y-%m-%d %H:%M')})
	return render(request, 'add_space_poster.html', {'form': form})

def space_posters(request):
	context = {}
	context['posters'] = []
	for poster in Poster.objects.all():
		context['posters'].append(poster)
	context['leaders'] = []
	return render (request, 'space_posters.html', context)