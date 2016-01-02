from django.contrib import admin
from polls.models import NewSemester, PieceOfMusic, Feature, Vote

class NewSemesterAdmin(admin.ModelAdmin):
	list_display = ('user','next_semester', 'plans', 'engage')
	# ordering = ('-id',)

admin.site.register(PieceOfMusic)
admin.site.register(Feature)
admin.site.register(Vote)
admin.site.register(NewSemester, NewSemesterAdmin)