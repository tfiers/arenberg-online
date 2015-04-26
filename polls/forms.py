# coding: utf-8

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.forms import ModelForm
from polls.models import ZaventemTransport

class NewSemesterPoll(forms.Form):

	name_input = forms.CharField(
		label = _("Je naam"),
		widget = forms.TextInput(
			attrs={'placeholder': _("Voor & Achter")}),
	)

	plans_input = forms.CharField(
	    label = _("Je plannen"),
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
						"met een sterk nieuw programma. In het tweede semester plannen " \
						"we een samenwerking met het Gents Universitair Koor, met concerten " \
						"in Leuven en in Gent. Om een goede bezetting te kunnen voorzien, " \
						"vragen we je nu al naar je plannen.</p>")),
				css_class="col-sm-offset-3 col-sm-6",
			),
			css_class="form-group space-below",
		),
		Field('name_input'),
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
			Submit(name='submit', value="Submit form", css_class="btn-success "),
			css_class="text-center",
		),
	)


class ZaventemTransportForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ZaventemTransportForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout.append(Submit(name='submit', value="Go", css_class="btn-success"))
	class Meta:
		model = ZaventemTransport
		fields = ['transport']
		labels = {
			'transport': _("Ik ga naar Zaventem ..")
		}