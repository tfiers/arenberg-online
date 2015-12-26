from django import forms
from music_suggestions.models import PieceOfMusic

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import FormActions, StrictButton

class SuggestPieceOfMusicForm(forms.ModelForm):
	class Meta:
		model=PieceOfMusic
		exclude=['suggested_by', 'suggested_by_string']
		labels = {
			'title': "Titel",
			'link_to_recording': "Link naar opname",
			'sheet_music': "Partituren",
		}
		help_texts = {
			'title':"Bijvoorbeeld \"Ludwig van Beethoven - Allegro Con Brio uit Symfonie No. 5\".",
			'link_to_recording':"Een YouTube URL bijvoorbeeld.",
			'sheet_music': ("Hier kan je eventueel meegeven hoe we aan de partituren kunnen geraken. "
	    "Je kan bijvoorbeeld een link geven naar IMSLP, naar een online muziekwinkel "
	    "(bv. bij halleonard.com of jwpepper.com) of naar een stuk op MuseScore (https://musescore.com/sheetmusic). "
	    "Heb jij de partituur? Heeft ons orkest de partituur al? "
	    "Gaat het enkel om een directiepartij ('score'), enkel om de 'parts', of om beide ('score+parts')? "
	    "Hebben we papieren en/of ingescande versies, of hebben we ook digitale semantische versies (MusicXML, MuseScore, Sibelius, Finale)?"),
		}
	helper = FormHelper()
	helper.form_action = 'music_suggestions:suggest'
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-2'
	helper.field_class = 'col-sm-8'
	helper.layout = Layout(
		'title',
		'link_to_recording',
		'sheet_music',
		FormActions(
			Submit('submit', 'Stel voor', css_class="btn-danger"),
		),

	)