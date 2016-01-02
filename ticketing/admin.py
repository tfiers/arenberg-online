from django.contrib import admin
from ticketing.models import (
	Production, Performance, PriceCategory, Ticket, Order, 
	StandardMarketingPollAnswer, GivenPaperTickets )
from import_export.resources import ModelResource
from import_export.admin import ImportExportModelAdmin
from import_export import fields

class OrderResource(ModelResource):
	# num_tickets = fields.Field()
	# total_price = fields.Field()
	num_student_tickets = fields.Field()
	num_non_student_tickets = fields.Field()
	num_culture_card_tickets = fields.Field()
	num_zaventem_tickets = fields.Field()

	# def dehydrate_num_tickets(self, order):
	# 	return order.num_tickets()

	# def dehydrate_total_price(self, order):
	# 	return order.total_price()

	def dehydrate_num_student_tickets(self, order):
		return Ticket.objects.filter(order=order, price_category=PriceCategory.objects.get(
			full_name="Student VVK (vanaf winter 2014)", price=5)).count()

	def dehydrate_num_non_student_tickets(self, order):
		return Ticket.objects.filter(order=order, price_category=PriceCategory.objects.get(
			full_name="Niet-student in VVK (vanaf winter 2014)", price=9)).count()

	def dehydrate_num_culture_card_tickets(self, order):
		return Ticket.objects.filter(order=order, price_category=PriceCategory.objects.get(
			full_name="KU Leuven Cultuurkaart in VVK (vanaf winter 2014)", price=4)).count()

	class Meta:
		model = Order
		fields = ('performance__short_name', 'online', 'first_name', 'last_name', 'email', 'payment_method', 'user_remarks',)


class OrderAdmin(ImportExportModelAdmin):
	resource_class = OrderResource
	list_display = ('first_name', 'last_name', 'seller', 'num_tickets', 'total_price',
		'performance', 'payment_method', 'email', 'date', 'user_remarks', 'admin_remarks',)
	ordering = ('-date',)
	list_per_page = 1000

class StandardMarketingPollAnswerAdmin(admin.ModelAdmin):
	list_display = ('associated_order', 'marketing_feedback', 'referred_member', 'first_concert',)
	list_per_page = 1000

admin.site.register(Production)
admin.site.register(Performance)
admin.site.register(PriceCategory)
admin.site.register(Order, OrderAdmin)
admin.site.register(Ticket)
admin.site.register(StandardMarketingPollAnswer, StandardMarketingPollAnswerAdmin)
admin.site.register(GivenPaperTickets)
