from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions, PrependedText

class NewSemesterPoll(forms.Form):

	name_input = forms.CharField(
		label = "Je naam",
	)

	plans_input = forms.CharField(
	    widget = forms.Textarea(),
	    label = "Je plannen",
	)

	next_semester_input = forms.BooleanField(
		label = "Ik speel volgend semester mee in het orkest",
		required = False,
	)

	engage_input = forms.BooleanField(
		label = "Ik wil verantwoordelijkheid opnemen voor een taak in de organisatie",
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
				HTML(("<p>Volgend semester same as usual: een concertreeks in Leuven, "
					  "met een sterk nieuw programma. In het tweede semester plannen "
					  "we een samenwerking met het Gents Universitair Koor, met concerten "
					  "in Leuven en in Gent. Om een goede bezetting te kunnen voorzien, "
					  "vragen we je nu al naar je plannen.</p>")),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group",
		),
		Field('name_input', placeholder="Voor & Achter"),
		Field('plans_input', rows="3", placeholder=("Tot wanneer plan je in het Arenbergorkest te spelen? "
	    			 'Bijvoorbeeld: "Tot het einde van mijn master", "Dit is m\'n laatste semester" of '
	    			 '"Nog tot en met volgend semester"')),
		# The next form inputs require the dev-version of django-crispy-forms to be layouted correctly.
		# (Specifically, this commit: https://github.com/maraujop/django-crispy-forms/commit/5c3a268)
		# Install this dev version with (pip and git required on path):
		# pip install -e git+git://github.com/maraujop/django-crispy-forms.git@dev#egg=django-crispy-forms
		Div(
			Div(
				HTML("<p>Concreet voor volgend semester (vink even aan):</p>"),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group spacer",
		),
		'next_semester_input',
		Div(
			Div(
				HTML("<p>Er volgt nog meer info over wat je kan doen, maar als je het nu al weet:</p>"),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group spacer",
		),
		'engage_input',
		FormActions(
			Submit('submit', 'Gaan met die banaan', css_class="btn-success"),
		),
	)
