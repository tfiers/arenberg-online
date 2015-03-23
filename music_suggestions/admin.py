from django.contrib import admin
from music_suggestions.models import PieceOfMusic, Vote

admin.site.register(PieceOfMusic)
admin.site.register(Vote)
