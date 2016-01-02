from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from polls.forms import NewSemesterPoll, SuggestPieceOfMusicForm, SuggestFeatureForm
from polls.models import NewSemester, PieceOfMusic, Feature, Vote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import User
import gc

def thanks(request):
	return render(request, 'thanks.html')

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def new_semester(request):
	#prevents UNIQUE constraint failed by filling same form out twice
	if NewSemester.objects.filter(user=request.user):
		return HttpResponseRedirect(reverse('polls:thanks'))
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
			return HttpResponseRedirect(reverse('polls:thanks'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = NewSemesterPoll()

	response = render(request, 'new_semester.html', {'form': form})
	# Workaround to correctly translate the value of the submit button in the form.
	response.content = response.content.replace("Submit form", (_("Gaan met die banaan")).encode('utf-8'))
	return response

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def browse_suggested_pieces(request, titlelike=None):
	pieces = []
	likes = []
	liked = []
	pi = PieceOfMusic.objects.all().order_by('title')
	iterator = queryset_iterator(pi)
	#conditions for creating a vote object
	if titlelike != None:
		voteobject = Vote.objects.filter(receiving_piece__title=titlelike,voter=request.user)
		titlepiece = PieceOfMusic.objects.get(title=titlelike)
		if (not voteobject) and titlepiece:
			Vote.objects.create(receiving_piece=titlepiece,voter=request.user)
		elif voteobject and titlepiece:
			voteobject.delete()
	#listing every suggested piece and its votes
	#if pi is a safety measure, the query_set iterator cannot handle empty querysets
	if pi:
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
	else:
		zipped=None
	return render(request,'browse_suggested_pieces.html',{'suggested_pieces': zipped})

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def suggest_piece(request):
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
			return HttpResponseRedirect(reverse('polls:browse'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = SuggestPieceOfMusicForm()

	return render(request,
		'suggest_piece_of_music.html',
		{'form': form})

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def browse_features(request, titlelike=None):
	features = Feature.objects.all()
	return render(request,'browse_suggested_features.html',{'features': features})

@login_required
@user_passes_test(lambda u:u.approved,login_url='/accessrestricted')
def suggest_feature(request):
	# If this is a POST request we need to process the form data.
	if request.method == 'POST':
		# Create a MODELform instance and populate it with data from the request:
		form = SuggestFeatureForm(request.POST)
		# If the data entered is valid, save it MODELform data to the database
		if form.is_valid():
			#commit is false to be able to add current user and such to the fields
			feat=form.save(commit=False)
			feat.suggested_by = request.user
			feat.save()
			return HttpResponseRedirect(reverse('polls:browse_feature'))

	# If this is a GET request (or any other type of request) we'll create a blank form.
	else:
		form = SuggestFeatureForm()

	return render(request,'suggest_feature.html',{'form': form})

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