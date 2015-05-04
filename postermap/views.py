from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from postermap.models import Poster
from ticketing.models import Production
from core.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, ChoiceField
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
		form.full_clean() 
		print form.cleaned_data.get("hanging_date", "nope")
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('space_ticketing:space_posters'))
	else:
		form = PosterForm(initial={'hanging_date': datetime.now().strftime('%Y-%m-%d %H:%M')})
	return render(request, 'add_space_poster.html', {'form': form})

@login_required
def space_posters(request):
	context = {}
	context['posters'] = []
	for poster in Poster.objects.all():
		context['posters'].append(poster)
	context['leaders'] = get_poster_leaders(request.user)
	return render (request, 'space_posters.html', context)

def get_poster_leaders(current_user):
	leaders = []
	for user in User.objects.all():
		# poster_locations = [p for p in Poster.objects.all() if user in p.authors]
		# Slow! Causes about 50 times more db queries as line below.
		poster_locations = Poster.objects.filter(Q(entered_by=user) | Q(hung_by=user))
		num_locations = len(poster_locations)
		num_posters = sum([p.count for p in poster_locations])
		data = {
			'leader': user,
			'num_locations': num_locations,
			'num_posters': num_posters,
			'score': 50*num_locations+10*num_posters,
		}
		leaders.append(data)
		if user == current_user:
			user_data = data
	leaders = sorted(leaders, key=lambda k: k['score'], reverse=True)
	ranking = sorted(list(set([leader['score'] for leader in leaders])), reverse=True)
	for leader in leaders:
		leader['rank'] = ranking.index(leader['score']) + 1
	top5 = leaders[0:5]
	if user_data in top5 or user_data['num_locations'] == 0:
		return top5
	else:
		return top5[0:4]+[user_data]