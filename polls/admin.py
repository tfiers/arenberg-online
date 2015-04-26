from django.contrib import admin
from polls.models import NewSemester
from polls.models import ZaventemTransport

class NewSemesterAdmin(admin.ModelAdmin):
	list_display = ('name', 'next_semester', 'plans', 'engage')
	ordering = ('-id',)

admin.site.register(NewSemester, NewSemesterAdmin)
admin.site.register(ZaventemTransport)