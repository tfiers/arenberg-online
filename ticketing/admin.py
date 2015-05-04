from django.contrib import admin
from ticketing.models import (
	Production, Performance, PriceCategory, Ticket, Order, 
	StandardMarketingPollAnswer, GivenPaperTickets )

class OrderAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'seller', 'num_tickets', 'total_price',
		'performance', 'payment_method', 'email', 'date', 'user_remarks', 'admin_remarks')
	ordering = ('-date',)
	list_per_page = 1000

class StandardMarketingPollAnswerAdmin(admin.ModelAdmin):
	list_display = ('associated_order', 'marketing_feedback', 'referred_member', 'first_concert')
	list_per_page = 1000

admin.site.register(Production)
admin.site.register(Performance)
admin.site.register(PriceCategory)
admin.site.register(Order, OrderAdmin)
admin.site.register(Ticket)
admin.site.register(StandardMarketingPollAnswer, StandardMarketingPollAnswerAdmin)
admin.site.register(GivenPaperTickets)
