from django.shortcuts import render
from surfice.models import Surf, Surfice, Status, Ding, Event
from django.http import HttpResponse

def ajax(request):
	print "hi"
	return HttpResponse("hello")