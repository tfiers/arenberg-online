from django.contrib import admin
from ticketing.models import (
	Production, Performance, PriceCategory, Ticket, Order, 
	StandardMarketingPollAnswer, GivenPaperTickets )
from import_export.resources import ModelResource
from import_export.admin import ImportExportModelAdmin

class OrderResource(ModelResource):
    class Meta:
        model = Order

class OrderAdmin(ImportExportModelAdmin):
	resource_class = OrderResource
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
