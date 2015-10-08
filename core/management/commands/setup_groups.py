from django.core.management.base import BaseCommand
from core.models import Group, AlternativeGroupName
from datetime import datetime
import django.utils.timezone as django_tz

def make_group(name, *alternative_names):
	# 'update_or_create' returns a tuple (object, created)
	# We only want the object, thus the '[0]'.
	group = Group.objects.update_or_create(name=name)[0]
	for alternative_name in alternative_names:
		AlternativeGroupName.objects.update_or_create(name=alternative_name, group=group)
	return group

help_string = ('Creates a basic set of Groups for the orchestra, if they '
			   'do not exist yet.')
def setup_groups():
	violen_1 		= make_group("violen_1", 		"violen1", "viool1", "1e_violen")
	violen_2		= make_group("violen_2", 		"violen2", "viool2", "2e_violen")
	violen  		= make_group("violen", 			"viool")
	violen.children.add(violen_1, violen_2)
	altviolen 		= make_group("altviolen", 		"altviool")
	celli 			= make_group("celli", 			"cello")
	contrabassen	= make_group("contrabassen",	"contrabas", "bas", "bassen")
	strijkers 		= make_group("strijkers", 		"")
	strijkers.children.add(violen, altviolen, celli, contrabassen)

	fluiten 		= make_group("fluiten", 		"fluit", "dwarsfluit", "dwarsfluiten")
	piccolo  		= make_group("piccolo", 		"piccoli")
	fluiten.children.add(piccolo)
	klarinetten		= make_group("klarinetten", 	"klarinet")
	basklarinet		= make_group("basklarinet", 	"basklarinetten")
	klarinetten.children.add(basklarinet)
	hobos			= make_group("hobos", 			"hobo")
	althobo			= make_group("althobo", 		"althobos")
	hobos.children.add(althobo)
	fagotten		= make_group("fagotten", 		"fagot")
	contrafagot		= make_group("contrafagot", 	"contrafagotten")
	fagotten.children.add(contrafagot)
	houtblazers		= make_group("houtblazers", 	"hout", "houten")
	houtblazers.children.add(fluiten, klarinetten, hobos, fagotten)

	hoorns	 		= make_group("hoorns", 			"hoorn")
	trompetten		= make_group("trompetten", 		"trompet")
	trombones		= make_group("trombones", 		"trombone")
	bastrombone		= make_group("bastrombone", 	"bastrombones")
	trombones.children.add(bastrombone)
	saxofoons		= make_group("saxofoons", 		"saxofoon", "saxen", "sax")
	bariton			= make_group("bariton", 		"baritons")
	euphonium		= make_group("euphonium", 		"euphoniums", "euphonia", "tenortuba", "eufonium", "eufonia", "eufoniums")
	bastuba			= make_group("bastuba", 		"bastubas")
	tubas			= make_group("tubas", 			"tuba")
	tubas.children.add(euphonium, bastuba)
	baritonsax		= make_group("baritonsax", 		"baritonsaxofoon")
	saxofoons.children.add(baritonsax)
	laag_koper		= make_group("laag_koper",		"lage_koperblazers")
	laag_koper.children.add(trombones, bariton, tubas, baritonsax)
	koperblazers	= make_group("koperblazers", 	"koper")
	koperblazers.children.add(hoorns, trompetten, trombones, saxofoons, bariton, tubas, baritonsax)

	blazers			= make_group("blazers")
	blazers.children.add(houtblazers, koperblazers)

	slagwerkers		= make_group("slagwerkers", 	"slagwerk", "percussie")

	harp			= make_group("harp",			"harpen")
	piano			= make_group("piano",			"toetsinstrumenten", "klavier", "keyboard", "celesta", "synthesizer")
	gitaren			= make_group("gitaren", 		"gitaar")
	basgitaar		= make_group("basgitaar", 		"basgitaren")
	gitaren.children.add(basgitaar)

	dirigent		= make_group("dirigent")

	orkest			= make_group("orkest", 			"volledig_orkest")
	orkest.children.add(strijkers, blazers, slagwerkers, harp, piano, gitaren, dirigent)

	# pv = pupiterverantwoordelijke
	# instrument in enkelvoud, omdat het om de "cello-pupiter" gaat.
	pv_list = [
		make_group("concertmeester", 	"pv_viool1", "verantwoordelijke_viool1", 	"pupitermeester_viool1")
		make_group("pv_viool2",			"verantwoordelijke_viool2", 				"pupitermeester_viool2")
		make_group("pv_altviool",		"verantwoordelijke_altviool", 				"pupitermeester_altviool")
		make_group("pv_cello",			"verantwoordelijke_cello", 					"pupitermeester_cello")
		make_group("pv_contrabas",		"verantwoordelijke_contrabas", 				"pupitermeester_contrabas")
		make_group("pv_fluit",			"verantwoordelijke_fluit", 					"pupitermeester_dwarsfluit")
		make_group("pv_klarinet",		"verantwoordelijke_klarinet", 				"pupitermeester_klarinet")
		make_group("pv_hobo",			"verantwoordelijke_hobo", 					"pupitermeester_hobo")
		make_group("pv_fagot",			"verantwoordelijke_fagot", 					"pupitermeester_fagot")
		make_group("pv_hoorn",			"verantwoordelijke_hoorn", 					"pupitermeester_hoorn")
		make_group("pv_trompet",		"verantwoordelijke_trompet", 				"pupitermeester_trompet")
		make_group("pv_laag_koper",		"verantwoordelijke_laag_koper", 			"pupitermeester_trombone")
		make_group("pv_slagwerk",		"verantwoordelijke_slagwerk", 				"pupitermeester_slagwerk")
		make_group("pv_piano",			"verantwoordelijke_piano", 					"pupitermeester_piano")	
		make_group("pvs", 				"pupiterverantwoordelijken", 				"pupitermeesters")
	]
	pvs.children.add(*pv_list)

	groups_in_snowman = [
		violen1,
		violen2,
		altviolen,
		celli,
		contrabassen,
		fluiten,
		klarinetten,
		hobos,
		fagotten,
		trompetten,
		hoorns,
		trombones, 
		euphonium,
		bastuba,
		tubas
		laag_koper,
		piano,
		slagwerkers,
	] + pv_list

	snowman		= make_group("snowman")
	for group in groups_in_snowman:
		alternative_names = [x.name+".snowman" for x in group.alternativegroupname_set.all()]
		snowman_group = make_group(group.name+".snowman", *alternative_names)
		snowman.children.add(snowman_group)
		AlternativeGroupName.objects.update_or_create(name=name, group=pv)


class Command(BaseCommand):
	args = 'none'
	help = help_string

	def handle(self, *args, **options):
		setup_groups()
		self.stdout.write('Succesfully set-up Groups.')