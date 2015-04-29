from django.contrib import admin
from postermap.models import Poster

class PosterAdmin(admin.ModelAdmin):
	list_display = ('hanging_date', 'entered_on', 'location_name', 'count', 'entered_by', 'attachment_type', 'remarks')
	ordering = ('-entered_on',)
admin.site.register(Poster, PosterAdmin)