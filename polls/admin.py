from django.contrib import admin
from polls.models import NewSemesterAnswer

class NewSemesterAnswerAdmin(admin.ModelAdmin):
	list_display = ('name', 'next_semester', 'plans', 'engage')
	ordering = ('-id',)

admin.site.register(NewSemesterAnswer, NewSemesterAnswerAdmin)