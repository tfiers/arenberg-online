from django.contrib import admin
from ticketing.models import Production, Performance, PriceCategory, Ticket, Order

admin.site.register(Production)
admin.site.register(Performance)
admin.site.register(PriceCategory)
admin.site.register(Ticket)
admin.site.register(Order)
