# coding: utf-8

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from ticketing.models import Order, Ticket, Performance, PriceCategory

class SnowmanTicketingForm(forms.Form):
    # TODO: translate (back to english, then back to dutch)
    first_name = forms.CharField(label='Voornaam', max_length=75, required=False)
    last_name = forms.CharField(label='Achternaam', max_length=75, required=False)
    email = forms.EmailField(label='E-mailadres')
    child_tickets = forms.IntegerField(label='Kinderen (12 jaar en jonger)', help_text='(€ 5)', initial=0, min_value=0)
    adult_tickets = forms.IntegerField(label='Volwassenen', help_text='(€ 10)', initial=0, min_value=0)
    payment_method = forms.ChoiceField(label='Betalingswijze', choices=Order.payment_method_choices)
    remarks = forms.CharField(label='Opmerkingen', widget=forms.Textarea, required=False)

def order_snowman_tickets(request):
    # If this is a POST request we need to process the form data.
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        form = SnowmanTicketingForm(request.POST)
        # If the data entered is valid, save a new order and associated tickets 
        # for the feb 2015 performance of "The Snowman" to the database.
        if form.is_valid():
            order = Order.objects.create(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                date = timezone.now(),
                remarks = form.cleaned_data['remarks'],
                payment_method = form.cleaned_data['payment_method']
            )
            performance = Performance.objects.filter(production__name__contains='The Snowman')[0]
            for i in range(form.cleaned_data['child_tickets']):
                Ticket.objects.create(
                    performance = performance,
                    price_category = PriceCategory.objects.filter(price=5)[0],
                    order = order
                )
            for i in range(form.cleaned_data['adult_tickets']):
                Ticket.objects.create(
                    performance = performance,
                    price_category = PriceCategory.objects.filter(price=10)[0],
                    order = order
                )
            return HttpResponseRedirect('/thanks')

    # If this is a GET request (or any other type of request) we'll create a blank form.
    else:
        form = SnowmanTicketingForm()

    return render(request, 'snowman_ticketing.html', {'form': form})


def thanks_for_snowman(request):
    return render(request, 'snowman_thanks.html')