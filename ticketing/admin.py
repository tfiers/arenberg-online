from django.contrib import admin
from ticketing.models import (
	Production, Performance, PriceCategory, Ticket, Order, 
	StandardMarketingPollAnswer )

admin.site.register(Production)
admin.site.register(Performance)
admin.site.register(PriceCategory)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(StandardMarketingPollAnswer)
