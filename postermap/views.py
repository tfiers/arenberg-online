from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from postermap.models import Poster
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, HiddenInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PosterForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(PosterForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.layout.append(
			Submit(name='submit', value=_("Hang poster op"), css_class="btn-success"))
	class Meta:
		model = Poster
		fields = ['latitutde', 'longitude', 'hanging_date', 'location_name', 
				  'count', 'hung_by', 'remarks', 'attachment_type']
		widgets = {'latitude': HiddenInput(), 'longitude': HiddenInput()}
		# labels = {
		# 	'transport': _("Ik ga naar Zaventem ..")
		# }

@login_required
def add_space_poster(request):
	if request.method == 'POST':
		pass
	else:
		form = PosterForm()
	return render(request, 'add_space_poster.html', {'form': form})