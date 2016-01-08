# coding: utf-8

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field, Button, Row
from crispy_forms.bootstrap import FormActions, StrictButton
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.forms import ModelForm
from polls.models import PieceOfMusic, Feature

class NewSemesterPoll(forms.Form):

	plans_input = forms.CharField(
	    label = _("Je plannen"),
	    required = True,
	    # Using the crispy-forms shortcut to specify the placeholder escapes the special characters twice.
	    widget = forms.Textarea(
	    	attrs={'placeholder': _('Tot wanneer plan je in het Arenbergorkest te spelen? ' \
			    			 		'Bijvoorbeeld: "Tot het einde van mijn master", "Nog tot en met volgend semester", of ' \
			    					'"Dit is m\'n laatste semester"')}),
	)

	next_semester_input = forms.BooleanField(
		label = _("Ik speel volgend semester mee in het orkest"),
		required = False,
	)

	engage_input = forms.BooleanField(
		label = _("Ik wil een functie opnemen in de organisatie"),
		required = False,
	)

	helper = FormHelper()
	helper.form_action = 'new_semester_poll'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-3'
	helper.field_class = 'col-sm-6'
	helper.layout = Layout(
		Div(
			Div(
				HTML(_(u"<p>Volgend semester creëren we opnieuw een concertreeks voor in Leuven, " \
						"met een sterk nieuw programma. Om een goede bezetting te kunnen garanderen vragen we nu al naar je plannen.</p>")),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group space-below",
		),
		Field('plans_input', rows="3"),
		# The next form inputs require the dev-version of django-crispy-forms, to be layouted correctly.
		# (Specifically, this commit: https://github.com/maraujop/django-crispy-forms/commit/5c3a268)
		# Install this dev version with (pip and git required on path):
		# pip install -e git+git://github.com/maraujop/django-crispy-forms.git@dev#egg=django-crispy-forms
		Div(
			Div(
				HTML(_("<p>Concreet voor volgend semester (vink even aan als van toepassing):</p>")),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group spacer",
		),
		'next_semester_input',
		Div(
			Div(
				HTML(_("<p>Er volgt nog meer info over wat je kan doen, maar als je het nu al weet:</p>")),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group spacer",
		),
		'engage_input',
		FormActions(
			# Note: using _("Gaan met die banaan") for the button label (value) doesn't work.
			# The same string apears in both the English and Dutch versions.
			# See views.py for the workaround we use for this.
			Submit(name='submit', value="Submit form", css_class="btn-danger"),
			css_class="text-center",
		),
	)

class SuggestPieceOfMusicForm(forms.ModelForm):
	class Meta:
		model=PieceOfMusic
		exclude=['suggested_by', 'suggested_by_string']
		labels = {
			'title': _("Titel"),
			'link_to_recording': _("Link naar opname"),
			'sheet_music': _("Partituren"),
		}
		help_texts = {
			'title':_("Bijvoorbeeld \"Ludwig van Beethoven - Allegro Con Brio uit Symfonie No. 5\"."),
			'link_to_recording':_("Een YouTube URL bijvoorbeeld."),
			'sheet_music': _("Hier kan je eventueel meegeven hoe we aan de partituren kunnen geraken. "
	    "Je kan bijvoorbeeld een link geven naar IMSLP, naar een online muziekwinkel "
	    "(bv. bij halleonard.com of jwpepper.com) of naar een stuk op MuseScore (https://musescore.com/sheetmusic). "
	    "Heb jij de partituur? Heeft ons orkest de partituur al? "
	    "Gaat het enkel om een directiepartij ('score'), enkel om de 'parts', of om beide ('score+parts')? "
	    "Hebben we papieren en/of ingescande versies, of hebben we ook digitale semantische versies (MusicXML, MuseScore, Sibelius, Finale)?"),
		}
	helper = FormHelper()
	helper.form_action = 'polls:suggest'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-2'
	helper.field_class = 'col-sm-8'
	helper.layout = Layout(
		'title',
		'link_to_recording',
		'sheet_music',
		FormActions(
			Submit('submit', _('Stel voor'), css_class="btn-danger"),
		),

	)

class SuggestFeatureForm(forms.ModelForm):
	class Meta:
		model=Feature
		exclude=['suggested_by'] #, 'suggested_by_string'
		labels = {
			'name': _("Idee"),
			'description': _('Beschrijving idee'),
		}
		help_texts = {
			'name':_("Welk idee is het?"),
			'desciption':_("Uitgebreide beschrijving!."),
		}
	helper = FormHelper()
	helper.form_action = 'polls:suggest_feature'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-2'
	helper.field_class = 'col-sm-8'
	helper.layout = Layout(
		'name',
		'description',
		FormActions(
			Submit('submit', _('Stel voor'), css_class="btn-danger"),
		),

	)