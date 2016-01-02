# coding: utf-8
from django.shortcuts import render

def landing(request):
	return render(request, 'snowman2016/landing.html')