from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from core.models import User
from music_suggestions.models import PieceOfMusic
from music_suggestions.forms import SuggestPieceOfMusicForm
from django.contrib.auth.decorators import login_required

@login_required
def browse_suggested_pieces(request):
	return render(request, 
		'browse_suggested_pieces.html', 
		{'suggested_pieces': PieceOfMusic.objects.all()})

@login_required
def suggest_piece(request):
	# If this is a POST request we need to process the form data.
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request:
		form = SuggestPieceOfMusicForm(request.POST)
		# If the data entered is valid, save a new music piece suggestion
		# to the database.
		if form.is_valid():
			piece=form.save(commit=False)
			piece.suggested_by = request.user
			piece.suggested_by_string = str(request.user.first_name) + " " + str(request.user.last_name)
			piece.save()
			return HttpResponseRedirect(reverse('music_suggestions:browse'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = SuggestPieceOfMusicForm()

	return render(request,
		'suggest_piece_of_music.html',
		{'form': form})