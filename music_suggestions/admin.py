from django.contrib import admin
from music_suggestions.models import PieceOfMusic, Feature, Vote

admin.site.register(PieceOfMusic)
admin.site.register(Feature)
admin.site.register(Vote)
