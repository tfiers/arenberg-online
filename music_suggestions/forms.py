from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import FormActions, StrictButton

class SuggestPieceOfMusicForm(forms.Form):
	title_input = forms.CharField(
		label = "Titel",
		help_text = "Bijvoorbeeld \"Ludwig van Beethoven - Allegro Con Brio uit Symfonie No. 5\".",
	)
	
	url_input = forms.URLField(
		label = "Link naar opname",
		help_text = "Een YouTube URL bijvoorbeeld.",
	)

	sheet_music_input = forms.CharField(
	    widget = forms.Textarea(),
	    label = "Partituren",
	    help_text = ("Hier kan je eventueel meegeven hoe we aan de partituren kunnen geraken. "
	    "Je kan bijvoorbeeld een link geven naar IMSLP, naar een online muziekwinkel "
	    "(bv. bij halleonard.com of jwpepper.com) of naar een stuk op MuseScore (https://musescore.com/sheetmusic). "
	    "Heb jij de partituur? Heeft ons orkest de partituur al? "
	    "Gaat het enkel om een directiepartij ('score'), enkel om de 'parts', of om beide ('score+parts')? "
	    "Hebben we papieren en/of ingescande versies, of hebben we ook digitale semantische versies (MusicXML, MuseScore, Sibelius, Finale)?"),
	    required = False,
	)

	name_input = forms.CharField(
		label = "Je naam",
	)

	helper = FormHelper()
	helper.form_action = 'music_suggestions:suggest'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-2'
	helper.field_class = 'col-sm-8'
	helper.layout = Layout(
		'title_input',
		'url_input',
		'sheet_music_input',
		FormActions(
			Submit('submit', 'Stel voor', css_class="btn-success"),
		),

	)
