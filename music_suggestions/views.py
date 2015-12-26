from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from core.models import User
from music_suggestions.models import PieceOfMusic, Vote
from music_suggestions.forms import SuggestPieceOfMusicForm
from django.contrib.auth.decorators import login_required
import gc

@login_required
def browse_suggested_pieces(request, titlelike=None):
	if not request.user.approved:
		return HttpResponseRedirect(reverse('notapproved'))
	pieces = []
	likes = []
	liked = []
	iterator = queryset_iterator(PieceOfMusic.objects.all().order_by('title'))
	#conditions for creating a vote object
	if titlelike != None:
		voteobject = Vote.objects.filter(receiving_piece__title=titlelike,voter=request.user)
		titlepiece = PieceOfMusic.objects.get(title=titlelike)
		if (not voteobject) and titlepiece:
			Vote.objects.create(receiving_piece=titlepiece,voter=request.user)
		elif voteobject and titlepiece:
			voteobject.delete()
	#listing every suggested piece and its votes
	for p in iterator: 
		#get piece
		pieces.append(p)
		#get number of total votes
		votes = Vote.objects.filter(receiving_piece__title=p.title).count() #the amount of vote objects in every index number of the list is counted in the template
	   	likes.append(votes)
	   	#did user like it him-/herself?
	   	voted = Vote.objects.filter(receiving_piece__title=p.title,voter=request.user)
	   	if voted:
	   		liked.append(True)
	   	else:
	   		liked.append(False)
   	zipped = zip(pieces,likes,liked)
	return render(request,'browse_suggested_pieces.html',{'suggested_pieces': zipped, "liked":liked})

@login_required
def suggest_piece(request):
	if not request.user.approved:
		return HttpResponseRedirect(reverse('notapproved'))
	# If this is a POST request we need to process the form data.
	if request.method == 'POST':
		# Create a MODELform instance and populate it with data from the request:
		form = SuggestPieceOfMusicForm(request.POST)
		# If the data entered is valid, save it MODELform data to the database
		if form.is_valid():
			#commit is false to be able to add current user and such to the fields
			piece=form.save(commit=False)
			piece.suggested_by = request.user
			piece.suggested_by_string = str(request.user.first_name) + " " + str(request.user.last_name)
			piece.save()
			Vote.objects.create(receiving_piece=piece,voter=request.user) #immediately create the submitting users vote
			return HttpResponseRedirect(reverse('music_suggestions:browse'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = SuggestPieceOfMusicForm()

	return render(request,
		'suggest_piece_of_music.html',
		{'form': form})

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